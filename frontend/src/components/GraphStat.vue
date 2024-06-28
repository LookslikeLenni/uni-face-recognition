<script>
import { VNetworkGraph, VEdgeLabel } from "v-network-graph";
import "v-network-graph/lib/style.css";
import { mapState, mapActions } from "vuex";
import { reactive } from "vue";
import * as vNG from "v-network-graph";
import { ForceLayout } from "v-network-graph/lib/force-layout";

export default {
  components: {
    VNetworkGraph,
    VEdgeLabel,
  },
  computed: {
    ...mapState('StatisticGraphStore', ['nodes', 'edges']),
  },
  methods: {
    ...mapActions('StatisticGraphStore', ['getGraphData']),
    async fetchGraphData() {
      await this.getGraphData();
    },
  },
  data() {
    const configs = reactive(
      vNG.defineConfigs({
        view: {
          layoutHandler: new ForceLayout({
            positionFixedByDrag: false,
            positionFixedByClickWithAltKey: true,
            createSimulation: (d3, nodes, edges) => {
              const forceLink = d3.forceLink(edges).id(d => d.id);
              return d3
                .forceSimulation(nodes)
                .force("edge", forceLink.distance(40).strength(0.1))
                .force("charge", d3.forceManyBody().strength(-200))
                .force("center", d3.forceCenter().strength(0.5))
                .alphaMin(0.001);
            },
          }),
        },
        node: {
          selectable: true,
          normal: {
            radius: node => Math.min(30, Math.max(10, node.timeInFrame / 100)), // Scale the radius
            color: "red",
          },
          hover: {
            color: "yellow",
            
          },
          label: {
            show: true,
            color: "white",
            fontSize: 12,
          },
        },
        edge: {
          selectable: true,
          hoverable: true,
          normal: {
            color: "red",
            width: edge => edge.width, // Use width from edge data
          },
          hover: {
            color: "yellow",
            width: 2,
          },
          label: {
            fontSize: 11,
            color: "transparent",  // Match the background color
          },
        },
      })
    );
    return { configs };
  },
  created() {
    this.fetchGraphData();
  },
};
</script>

<template>
  <div class="graph">
    <v-network-graph 
      v-if="Object.keys(nodes).length && Object.keys(edges).length" 
      :nodes="nodes" 
      :edges="edges" 
      :configs="configs"
    >
      <template #edge-label="{ edge, hovered, selected, ...slotProps }">
        <v-edge-label
          :class="{ hovered, selected }"
          :text="edge.timeTogether + 's'"
          align="center"
          vertical-align="above"
          v-bind="slotProps"
        />
      </template>
    </v-network-graph>
  </div>
</template>


<style scoped>
.graph {
  width: 80%;
  height: 600px;
  border: 1px solid #000;
  margin: 0 auto;
}

/* Edge Lables */
:deep(.v-ng-edge-label) {
  transition: fill 0.1s;
  fill: transparent; /* Match the background color */
}
:deep(.v-ng-edge-label.hovered) {
  fill: white;
  font-weight: bold;
}
:deep(.v-ng-edge-label.selected) {
  fill: white; /* Change to white when selected */
  font-weight: bold;
}


</style>

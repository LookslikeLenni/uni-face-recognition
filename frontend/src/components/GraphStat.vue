<template>
  <div class="graph">
    <v-network-graph 
      v-if="Object.keys(nodes).length && Object.keys(links).length" 
      :nodes="nodes" 
      :edges="links" 
      :configs="configs"
    >
      <template #edge-label="{ edge, ...slotProps }">
        <v-edge-label :text="edge.label" align="center" vertical-align="above" v-bind="slotProps" />
      </template>
    </v-network-graph>

  </div>
</template>

<script>
import { VNetworkGraph } from "v-network-graph";
import "v-network-graph/lib/style.css";
import { mapState, mapActions } from "vuex";
import * as vNG from "v-network-graph";

export default {
  components: {
    VNetworkGraph,
  },
  computed: {
    ...mapState('StatisticGraphStore', ['nodes', 'links']),
  },
  methods: {
    ...mapActions('StatisticGraphStore', ['getGraphData']),

    async fetchGraphData() {
      await this.getGraphData();
      this.$nextTick(() => {
        console.log("Nodes:", JSON.stringify(this.nodes, null, 2));
        console.log("Links:", JSON.stringify(this.links, null, 2));
      });
    },
  },
  created() {
    this.fetchGraphData();
    this.configs = vNG.defineConfigs({
      node: {
        selectable: true,
        normal: {
          radius: 20,
          color: "red",
        },
        hover: {
          radius: 22,
        },
        label: {
          show: true,
          color: "white",
          fontSize: 12,
        },
      },
      edge: {
        normal: {
          color: "brown",
          width: 1,
          
        },
        hover: {
          color: "yellow",
          width: 2,
          label: edge => edge.width,
        },
      },
    });
  },
};
</script>

<style scoped>
.graph {
  width: 800px;
  height: 600px;
  border: 1px solid #000;
}
</style>

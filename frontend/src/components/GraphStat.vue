<template>
  <div>
    <v-network-graph 
      v-if="nodes.length && links.length" 
      :nodes="styledNodes" 
      :links="styledLinks" 
      
    />
  </div>
</template>

<script>
import { VNetworkGraph } from "v-network-graph";
import "v-network-graph/lib/style.css";
import { mapState, mapActions } from "vuex";
import * as vNG from "v-network-graph"

 const configs = vNG.defineConfigs({
  node: {
    selectable: true,
    normal: {
      radius: 10,
      color: "#ffffff",
      strokeColor: "#ff00dd",
      strokeWidth: 3,
    },
    hover: {
      radius: 14,
      color: "#ffffff",
      strokeColor: "#ff00dd",
      strokeWidth: 3,
    },
    label: {
      visible: false,
    },
    focusring: {
      color: "#ff00dd30", // alpha
    },
  },
  edge: {
    normal: {
      width: edge => (edge.animate ? 2 : 1),
      color: "#ff00dd",
      dasharray: edge => (edge.animate ? "4" : "0"),
      animate: edge => !!edge.animate,
    },
    hover: {
      color: "#ff00dd",
    },
  },
}) 

export default {
  components: {
    VNetworkGraph,
  },
  computed: {
    ...mapState('StatisticGraphStore', ['nodes', 'links']),
    styledNodes() {
      return this.nodes.map(node => ({
        ...node,
        color: 'white',
        label: node.label || '',  // Ensures label is present to style text
      }));
    },
    styledLinks() {
      return this.links.map(link => ({
        ...link,
        color: 'grey',
        width: this.scaleLinkWidth(link.timeTogether),
      }));
    },
  },
  methods: {
    ...mapActions('StatisticGraphStore', ['getGraphData']),
    async fetchGraphData() {
      await this.getGraphData();
      this.$nextTick(() => {
        console.log("Nodes:", this.styledNodes);
        console.log("Links:", this.styledLinks);
      });
    },
    scaleLinkWidth(timeTogether) {
      // Adjust this function as needed for appropriate scaling
      return Math.min(10, Math.max(1, timeTogether / 10));
    },
  },
  created() {
    this.fetchGraphData();
  },
};
</script>

<style scoped>

</style>
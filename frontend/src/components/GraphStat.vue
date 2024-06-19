<template>
  <div>
    <button @click="test">Test</button>
    <v-network-graph v-if="nodes.length && links.length" :nodes="nodes" :links="links" />
  </div>
</template>

<script>
  import { VNetworkGraph } from "v-network-graph";
  import "v-network-graph/lib/style.css";
  import { mapState, mapActions } from "vuex";

  export default {
    components: {
      VNetworkGraph,
    },
    computed: {
      ...mapState('StatisticGraphStore', ['nodes', 'links']),
    },
    methods: {
      ...mapActions('StatisticGraphStore', ['getGraphData']),
      async test() {
        await this.getGraphData();
        // Ensure that the state is updated before accessing it
        this.$nextTick(() => {
          console.log("Nodes:", this.nodes);
          console.log("Links:", this.links);
        });
      },
    },
  };
</script>

<style>
/* Add styles for v-network-graph components */
.v-network-graph__node {
  background-color: white;
  color: white; /* Font color */
  border: 2px solid grey; /* Node border color */
}

.v-network-graph__link {
  stroke: grey; /* Link color */
}

/* Additional style adjustments if needed */
.v-network-graph__label {
  color: white; /* Font color for labels */
}
</style>

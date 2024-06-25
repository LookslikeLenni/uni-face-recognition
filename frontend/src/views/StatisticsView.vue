<script>
import GraphStat from '../components/GraphStat.vue';
import LeaderBoard from '../components/LeaderBoard.vue';

export default {
  components: {
    GraphStat,
    LeaderBoard
  }
}
</script>

<template>
  <div>
    <h1>Statistics View</h1>
    <GraphStat />
    <LeaderBoard />
  </div>
</template>


<style>
@media (min-width: 1024px) {
  .about {
    min-height: 100vh;
    display: flex;
    align-items: center;
  }
}
</style>

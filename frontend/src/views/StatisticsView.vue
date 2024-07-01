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
  <div class="container">
    <div class="content">
      <GraphStat />
      <LeaderBoard />
    </div>
  </div>
</template> 

<style scoped>
.container {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -25%);
}

.content > *:not(:last-child) {
  margin-bottom: 20px; /* Adjust the gap size as needed */
}

</style>

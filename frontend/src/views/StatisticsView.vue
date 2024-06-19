<script>
import GraphStat from '../components/GraphStat.vue';

export default {
  components: {
    GraphStat
  }
}
</script>

<template>
  <div>
    <h1>Statistics View</h1>
    <GraphStat />
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

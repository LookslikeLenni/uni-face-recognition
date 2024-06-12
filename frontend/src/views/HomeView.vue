<script>
import LiveFeed from '../components/LiveFeed.vue'
import LiveChat from '../components/LiveChat.vue'

export default {
  components: {
    LiveFeed,
    LiveChat
  }
}
</script>

<template>
    <div class="center-content">
        <LiveFeed />
        <LiveChat />
    </div>
</template>

<style scoped>
.center-content {
    display: grid;
    grid-template-columns: 190% auto;
    justify-items: center;
    align-items: center;
    height: 100vh;
}
</style>

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
  <div class="container">
    <div class="row justify-content-center">
      <div class="col-md-8">
        <LiveFeed />
      </div>
      <div class="col-md-4">
        <LiveChat />
      </div>
    </div>
  </div>
</template>

<style scoped>
.container {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

.col-md-9, .col-md-3 {
  padding: 0; /* Optional: Remove padding if needed */
}
</style>

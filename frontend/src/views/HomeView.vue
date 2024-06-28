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
  <div class="home-view">
    <div class="stream-chat-container">
      <LiveFeed />
      <LiveChat />
    </div>
  </div>
</template>

<style>
.stream-chat-container {
  display: grid;
  place-items: center;
}

/* Assuming you want the live feed to take more space than the chat */
.LiveFeed {
  flex: 4; /* Adjust the ratio as needed */
}

.LiveChat {
  flex: 1; /* Adjust the ratio as needed */
}
</style>

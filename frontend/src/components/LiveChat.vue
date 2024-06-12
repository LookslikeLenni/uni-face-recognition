<script>
import { mapState, mapActions } from 'vuex';

export default {
  data() {
    return {
      isMuted: false,
    };
  },
  computed: {
    ...mapState('CurrentUsersStore', ['currentUsers'])
  },
  methods: {
    ...mapActions('CurrentUsersStore', ['fetchCurrents']),
    fetchMessages() {
      this.fetchCurrents(); 
      this.currentUsers.forEach(user => {
        this.readGreeting(user.greeting);
      });
    },
    readGreeting(greeting) {
      console.log('readGreeting called with:', greeting); // Debugging line
      if ('speechSynthesis' in window && !this.isMuted) {
        var msg = new SpeechSynthesisUtterance(greeting);
        window.speechSynthesis.speak(msg);
      } else {
        console.log('Your browser does not support speech synthesis or the chat is muted.');
      }
    },
    toggleMute() {
      this.isMuted = !this.isMuted;
    }
  },
  created() {
    this.fetchMessages();
    this.intervalId = setInterval(this.fetchMessages, 10000);
  },
  beforeDestroy() {
    clearInterval(this.intervalId);
  },
}
</script>

<template>
  <div class="live-chat"> Chat:
    <button @click="toggleMute">{{ isMuted ? 'Unmute' : 'Mute' }}</button>
    <transition name="fade">
      <div>
        <div v-for="user in currentUsers" 
            :key="user.id"
            class="message">
          <p>{{ user.first_name }}: {{ user.greeting }}</p>
        </div>
      </div>
    </transition>
  </div>
</template>

<!-- Your styles here -->

<style scoped>
.fade-exit-active {
  transition: opacity 1s;
  opacity: 0;
}

.message {
  border: 1px solid #000; /* Change as needed */
}

.live-chat {
  background-color: #0e0e10;
  color: #e0e0e0;
  width: 300px;
  height: 750px;
  overflow-y: scroll;
  padding: 10px;
  border-radius: 5px;
  font-family: Arial, sans-serif;
  font-size: 14px;
  line-height: 1.5;
}

.live-chat div {
  margin-bottom: 10px;
}

.live-chat p {
  margin: 0;
}
</style>

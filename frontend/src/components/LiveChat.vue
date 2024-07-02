<script>
import { mapState, mapMutations, mapActions } from 'vuex';

export default {
  data() {
    return {
      messageQueue: [],
      isSpeaking: false,
      intervalId: null,
      lastMessageTime: null, // Track the last message time
    };
  },
  computed: {
    ...mapState('CurrentUsersStore', ['currentUsers', 'isMuted']),
  },
  methods: {
    ...mapActions('CurrentUsersStore', ['fetchCurrents']),
    ...mapMutations('CurrentUsersStore', ['SET_MUTE_STATUS']),
	
    async fetchMessages() {
      clearInterval(this.intervalId);
      await this.fetchCurrents();
      const now = Date.now();
      this.currentUsers.forEach(user => {
        // Only add new messages based on a condition (e.g., timestamp)
        if (!this.lastMessageTime || new Date(user.lastMessageTime) > this.lastMessageTime) {
          this.addMessageToQueue(user.greeting);
        }
      });
      this.lastMessageTime = now; // Update the last message time

      if (!this.isSpeaking && !this.isMuted) { // Check if not muted before speaking
        this.speakNextMessage();
      }
      this.intervalId = setInterval(this.fetchMessages, 10000);
    },

    addMessageToQueue(message) {
      this.messageQueue.push(message);
    },
    speakNextMessage() {
      if (this.messageQueue.length === 0 || this.isMuted) { // Check mute status here as well
        this.isSpeaking = false;
        return;
      }
      this.isSpeaking = true;
      const message = this.messageQueue.shift();
      this.readGreeting(message);
    },
    readGreeting(greeting) {
      console.log('readGreeting called with:', greeting);
      if ('speechSynthesis' in window && !this.isMuted) {
        const msg = new SpeechSynthesisUtterance(greeting);
        msg.onend = () => {
          this.speakNextMessage();
        };
        window.speechSynthesis.speak(msg);
      } else {
        console.log('Your browser does not support speech synthesis or the chat is muted.');
      }
    },
    toggleMute() {
      const newMuteStatus = !this.isMuted;
      this.SET_MUTE_STATUS(newMuteStatus);
      if (newMuteStatus) {
        window.speechSynthesis.cancel();
        this.isSpeaking = false; // Ensure isSpeaking is set to false when muted
      } else {
        // Optionally, you might want to trigger speaking next message only under certain conditions
        if (this.messageQueue.length > 0) {
          this.speakNextMessage();
        }
      }
    },
    // Method to add a debug message
    sendDebugMessage() {
      const debugUser = {
        id: 'debug',
        first_name: 'Debug',
        greeting: 'This is a debug message',
        lastMessageTime: new Date().toISOString(),
      };
      this.currentUsers.push(debugUser);
      this.addMessageToQueue(debugUser.greeting);
      if (!this.isSpeaking && !this.isMuted) {
        this.speakNextMessage();
      }
    },
  },
  created() {
    this.fetchMessages();
  },
  beforeDestroy() {
    clearInterval(this.intervalId);
    if ('speechSynthesis' in window) {
      window.speechSynthesis.cancel();
    }
  },
}
</script>

<template>
  <div class="chat-container">
    <button class="mute-button" @click="toggleMute">{{ isMuted ? 'Unmute' : 'Mute' }}</button>
    <button class="debug-button" @click="sendDebugMessage">Send Debug Message</button>
    <transition name="fade">
      <div class="messages">
        <div v-for="user in currentUsers" 
             :key="user.id"
             class="message">
          <p><strong>{{ user.first_name }}:</strong> {{ user.greeting }}</p>
        </div>
      </div>
    </transition>
  </div>
</template>

<style scoped>
.chat-container {
  background-color: transparent;
  border: 2px solid #632c25; 
  border-radius: 10px;
  box-shadow: 0 2px 5px rgba(0,0,0,0.15);
  padding: 20px;
  width: 300px;
  max-width: 100%;
  margin: 0 auto;
  position: relative; /* This makes it a reference for the absolute positioning of the mute button */
}

.messages {
  max-height: 400px;
  overflow-y: auto;
  margin-top: 35px; /* Added margin to the top to move the container down */
  margin-right: 15%; /* Added margin to the right to prevent overlap */
}

.message {
  background-color: #282828;
  border-color:#a48484;
  border-radius: 10px;
  padding: 10px;
  margin-bottom: 10px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}

.mute-button, .debug-button {
  position: absolute;
  top: 10px;
  right: 10px;
  background-color: #292929;
  color: #ffffff;
  border: none;
  border-radius: 5px;
  padding: 5px 10px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.mute-button:hover, .debug-button:hover {
  background-color: #632c25;
}

.debug-button {
  right: 80px; /* Adjusted position to the left of the mute button */
}

.fade-enter-active, .fade-leave-active {
  transition: opacity 0.5s;
}

.fade-enter, .fade-leave-to {
  opacity: 0;
}
</style>



<script>
import { mapState, mapMutations, mapActions } from 'vuex';

export default {
  	data() {
		return {
		messageQueue: [],
		isSpeaking: false,
		};
	},
	computed: {
	...mapState('CurrentUsersStore', ['currentUsers', 'isMuted'])
	},
	methods: {
		...mapActions('CurrentUsersStore', ['fetchCurrents']),
		...mapMutations('CurrentUsersStore', ['SET_MUTE_STATUS']),
		async fetchMessages() {
			clearInterval(this.intervalId);
			await this.fetchCurrents(); 
			this.currentUsers.forEach(user => {
				this.addMessageToQueue(user.greeting);
			});
			if (!this.isSpeaking) {
				this.speakNextMessage();
			}
			this.intervalId = setInterval(this.fetchMessages, 10000);
		},
		addMessageToQueue(message) {
		this.messageQueue.push(message);
		},
		speakNextMessage() {
		if (this.messageQueue.length === 0) {
			this.isSpeaking = false;
			return;
		}
		this.isSpeaking = true;
		const message = this.messageQueue.shift();
		this.readGreeting(message);
		},
		readGreeting(greeting) {
		console.log('readGreeting called with:', greeting); // Debugging line
		if ('speechSynthesis' in window && !this.isMuted) {
			var msg = new SpeechSynthesisUtterance(greeting);
			msg.onend = () => {
			this.speakNextMessage();
			};
			console.log("before");
			window.speechSynthesis.speak(msg);
			console.log("after");
		} else {
			console.log('Your browser does not support speech synthesis or the chat is muted.');
		}
		},
		toggleMute() {
			const newMuteStatus = !this.isMuted;
			this.SET_MUTE_STATUS(newMuteStatus);
			if (newMuteStatus) {
				window.speechSynthesis.cancel();
			} else {
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

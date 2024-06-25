<template>
    <div class="leaderboard-container">
      <h1>Leaderboard</h1>
      <ul class="leaderboard-list">
        <li v-for="user in leaderboard" :key="user.id" class="leaderboard-item">
          {{ user.name }} - {{ user.timeInFrame.toFixed(2) }} seconds
        </li>
      </ul>
    </div>
  </template>
  
  <script>
  import { mapGetters } from 'vuex';
  
  export default {
    name: 'Leaderboard',
    computed: {
      ...mapGetters('StatisticGraphStore', ['getLeaderboard']),
      leaderboard() {
        console.log('Leaderboard:', this.getLeaderboard);
        return this.getLeaderboard;
      }
    },
  };
  </script>
  
  <style scoped>
  .leaderboard-container {
    width: 80%;
    margin: 0 auto;
    background: #212121;
    border-radius: 10px;
    padding: 20px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  }
  
  h1 {
    text-align: center;
    color: #ff0000;
    margin-bottom: 20px;
  }
  
  .leaderboard-list {
    list-style: none;
    padding: 0;
  }
  
  .leaderboard-item {
    background: #737373;
    padding: 10px 20px;
    margin: 10px 0;
    border-radius: 5px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  
  .leaderboard-item:nth-child(odd) {
    background: #3f3f3f;
  }
  </style>
  
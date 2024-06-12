<!-- AdminView.vue -->
<script>
import KnownFaces from '../components/KnownFaces.vue'
import AddingUnknownForm from '../components/AddingUnknownForm.vue'
import Log from '../components/Log.vue'


export default {
  data() {
    return {
      users: [],
    };
  },
  async mounted() {
    await this.fetchUsers();
  },
  methods: {
    async fetchUsers() {
      try {
        const response = await fetch('http://127.0.0.1:8000/users');
        const data = await response.json();
        this.users = Array.isArray(data) ? data : [];
      } catch (error) {
        console.error('Error fetching users:', error);
      }
    },
    reloadBothComponents() {
      this.fetchUsers();
    },
    
  },
  components: {
    KnownFaces,
    AddingUnknownForm,
    Log
  },
}
</script>

<template>
  <div class="admin-container">
      <div class="top-section">
          <KnownFaces :users="users" @reload-components="reloadBothComponents" />
          <AddingUnknownForm :users="users" @reload-components="reloadBothComponents" />
      </div>
      <div>
          <Log />
      </div>
  </div>
</template>

<style scoped>
.admin-container {
    display: flex;
    flex-direction: column;
    width: 100%;
}

.top-section {
    display: flex;
    justify-content: space-between;
}
</style>


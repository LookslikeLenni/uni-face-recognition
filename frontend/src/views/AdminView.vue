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
    <div class="Admin">
      <h1>This is an Admin page</h1>
    </div>
    <KnownFaces :users="users" />
    <AddingUnknownForm :users="users" @reload-components="reloadBothComponents" />
    <Log />
</template>
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
    updateUser(updatedUser) {
      const index = this.users.findIndex(user => user.id === updatedUser.id);
      if (index !== -1) {
        this.$set(this.users, index, updatedUser);
      }
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
    <AddingUnknownForm :users="users" />
    <Log />
</template>
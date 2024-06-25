<!-- AdminView.vue -->
<script>
import { onMounted } from 'vue';
import feather from 'feather-icons';
import KnownFaces from '../components/KnownFaces.vue';
import AddingUnknownForm from '../components/AddingUnknownForm.vue';
import Log from '../components/Log.vue';

export default {
  data() {
    return {
      users: [],
    };
  },
  async mounted() {
    await this.fetchUsers();
    feather.replace(); // Replace icons on mount
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
    async exportCSV() {
      try {
        const response = await fetch('http://127.0.0.1:8000/export/', { method: 'GET' });
        if (response.ok) {
          const blob = await response.blob();
          const url = window.URL.createObjectURL(blob);
          const a = document.createElement('a');
          a.href = url;
          a.download = 'users_images.csv';
          document.body.appendChild(a);
          a.click();
          a.remove();
        } else {
          console.error('Error exporting CSV:', response.statusText);
        }
      } catch (error) {
        console.error('Error exporting CSV:', error);
      }
    },
  },
  components: {
    KnownFaces,
    AddingUnknownForm,
    Log,
  },
};
</script>

<template>
  <div class="admin-container">
    <div class="top-section">
      <div class="identified-section">
        <KnownFaces :users="users" @reload-components="fetchUsers" />
      </div>
      <button @click="exportCSV" class="export-button">
        <i data-feather="download"></i>
      </button>
    </div>
    <div class="bottom-section">
      <AddingUnknownForm :users="users" @reload-components="fetchUsers" />
      <Log />
    </div>
  </div>
</template>

<style scoped>
.admin-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
}

.top-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  padding-top: 15px;
  position: relative;
}

.identified-section {
  flex: 1;
  text-align: center;
  border: 1px solid black;
  position: relative;
  overflow: hidden;
}

.identified-section::before {
  content: "Identified";
  position: absolute;
  top: 30px;
  left: 0;
  transform: translate(0, 0);
  font-size: 6rem;
  color: rgba(86, 86, 86, 0.3);
  white-space: nowrap;
  z-index: -1;
}

.export-button {
  position: absolute;
  top: 15px; /* Adjust to align with padding-top of top-section */
  right: 15px; /* Adjust for desired right margin */
  padding: 5px 10px; /* Smaller padding */
  font-size: 0.875rem; /* Smaller font size */
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #444;
  color: #fff;
  border: none;
}

.export-button:hover {
  background: #555;
}

.export-button i {
  width: 16px; /* Smaller icon size */
  height: 16px; /* Smaller icon size */
  stroke: currentColor;
  fill: none;
  stroke-width: 2;
}

.bottom-section {
  display: flex;
  text-align: center;
  padding-top: 15px;
  justify-content: space-between;
  width: 100%;
  border: 1px solid black;
  position: relative;
  overflow: hidden;
}

.bottom-section::before {
  content: "Unknown";
  position: absolute;
  top: 30px;
  left: 0;
  transform: translate(0, 0);
  font-size: 6rem;
  color: rgba(86, 86, 86, 0.3);
  white-space: nowrap;
  z-index: -1;
}
</style>

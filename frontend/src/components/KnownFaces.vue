<!-- KnownFaces.vue -->
<script>
export default {
  props: ['users'],
  data() {
    return {
      selectedUser: null,
      vieW: false,
      currentPage: 0,
      imagesPerPage: 69,
      newImages: []
    };
  },
  methods: {
    getUserImageUrl(userId, imageIndex) {
      imageIndex += this.currentPage * this.imagesPerPage;
      return `http://127.0.0.1:8000/users/${userId}/images/${imageIndex}/`;
    },
    nextPage() {
      if (this.currentPage === Math.ceil(this.selectedUser.images.length / this.imagesPerPage) - 1) {
        this.currentPage = 0;
      } else {
        this.currentPage++;
      }
    },
    prevPage() {
      if (this.currentPage === 0) {
        this.currentPage = Math.ceil(this.selectedUser.images.length / this.imagesPerPage) - 1;
      } else {
        this.currentPage--;
      }
    },
    async deleteUser(userId) {
      try {
        const confirmed = confirm("Are you sure you want to delete this user?");
        if (!confirmed) {
          return;
        }
        const response = await fetch(`http://127.0.0.1:8000/users/${userId}/`, {
          method: 'DELETE'
        });
        if (response.ok) {
          this.users = this.users.filter(user => user.id !== userId);
          console.log('User deleted');
        } else {
          console.error('Failed to delete user');
        }
      } catch (error) {
        console.error('Error deleting user:', error);
      }
    },
    selectUser(user) {
      this.selectedUser = {...user};
    },
    async updateUser() {
      try {
        console.log('Updating user:', this.selectedUser);
        let selectedUserID = this.selectedUser.id;
        const response = await fetch(`http://127.0.0.1:8000/users/${selectedUserID}/`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(this.selectedUser)
        });
        if (response.ok) {
          this.$emit('reload-components');
          this.selectedUser = null;
        } else {
          console.error('Failed to update user');
        }
      } catch (error) {
        console.error('Error updating user:', error);
      }
    },
    cancelEdit() {
      this.selectedUser = null;
      this.vieW = false;
      this.currentPage = 0;
      this.newImages = [];
    },
    downloadImagesZip(userId) {
      fetch(`http://127.0.0.1:8000/users/${userId}/images/zip/`, {
        method: 'GET',
      })
        .then(response => response.blob())
        .then(blob => {
          const url = window.URL.createObjectURL(blob);
          const a = document.createElement('a');
          a.href = url;
          a.download = `${this.selectedUser.first_name}-${this.selectedUser.last_name}-user-${userId}-images.zip`;
          document.body.appendChild(a); // Append the element to work in Firefox
          a.click();
          a.remove(); // Clean up
          window.URL.revokeObjectURL(url);
        })
        .catch(error => console.error('Error downloading images zip:', error));
    },
    handleImageUpload(event) {
        this.newImages = event.target.files;
    },
    async uploadImages() {
        try {
            const formData = new FormData();
            for (let i = 0; i < this.newImages.length; i++) {
            formData.append('image_files', this.newImages[i]);  // Ensure the key matches the backend parameter
            }
            const response = await fetch(`http://127.0.0.1:8000/users/${this.selectedUser.id}/images/`, {
            method: 'POST',
            body: formData
            });
            if (response.ok) {
            this.$emit('reload-components');
            this.newImages = [];
            alert('Images uploaded successfully');
            } else {
            const errorData = await response.json();
            console.error('Failed to upload images:', errorData.detail || errorData);
            }
        } catch (error) {
            console.error('Error uploading images:', error);
        }
    }
  },
  computed: {
    knownUsers() {
      return this.users.filter(user => user.first_name !== 'Unknown');
    }
  }
};
</script>

<template>
  <div>
    <div class="scrollable">
      <ul class="d-flex flex-wrap list-unstyled">
        <li
          v-for="user in knownUsers"
          :key="user.id"
          class="m-2"
          style="flex: 0 0 200px;"
        >
          <img :src="getUserImageUrl(user.id, 0)" alt="User Image" class="user-image img-thumbnail" />
          <div>
            <p>{{ user.id }}</p>
            <h3>{{ user.first_name }} {{ user.last_name }}</h3>
            <p>{{ user.greeting }}</p>
          </div>
          <button class="btn btn-outline-danger btn-sm" @click="deleteUser(user.id)">Delete</button>
          <button class="btn btn-outline-primary btn-sm" @click="selectUser(user)">Edit</button>
          <button class="btn btn-outline-secondary btn-sm" @click="selectUser(user); vieW = true">Images</button>
        </li>
      </ul>
    </div>
    <div v-if="selectedUser && !vieW" class="modal fade show" tabindex="-1" style="display: block;">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h2 class="modal-title">Edit User</h2>
            <button type="button" class="btn-close" @click="cancelEdit"></button>
          </div>
          <div class="modal-body">
            <input class="form-control mb-2" v-model="selectedUser.first_name" placeholder="First Name">
            <input class="form-control mb-2" v-model="selectedUser.last_name" placeholder="Last Name">
            <input class="form-control mb-2" v-model="selectedUser.greeting" placeholder="Greeting">
          </div>
          <div class="modal-footer">
            <button class="btn btn-outline-success" @click="updateUser">Save</button>
            <button class="btn btn-outline-secondary" @click="cancelEdit">Cancel</button>
          </div>
        </div>
      </div>
    </div>
    <div v-if="vieW && selectedUser" class="modal fade show" tabindex="-1" style="display: block;">
      <div class="modal-dialog" style="max-width: 90%;">
        <div class="modal-content">
          <div class="modal-header">
            <h2 class="modal-title">View Images ({{ selectedUser.images.length }} total)</h2>
            <button type="button" class="btn-close" @click="cancelEdit"></button>
          </div>
          <div class="modal-body">
            <div class="container-fluid">
              <div class="row">
                <div v-for="(image, index) in selectedUser.images.slice(currentPage * imagesPerPage, (currentPage + 1) * imagesPerPage)" :key="index" class="col-6 col-md-4 col-lg-2 col-xl-1 mb-3">
                  <img :src="getUserImageUrl(selectedUser.id, index)" alt="User Image" class="img-thumbnail user-image" />
                </div>
              </div>
            </div>
            <p class="text-center">Page {{ currentPage + 1 }} of {{ Math.ceil(selectedUser.images.length / imagesPerPage) }}</p>
          </div>
          <div class="modal-footer">
            <input type="file" multiple @change="handleImageUpload">
            <button class="btn btn-outline-success" @click="uploadImages">Upload Images</button>
            <button class="btn btn-outline-warning" @click="prevPage">Previous Page</button>
            <button class="btn btn-outline-warning" @click="nextPage">Next Page</button>
            <button class="btn btn-outline-secondary" @click="cancelEdit">Cancel</button>
            <button class="btn btn-outline-dark" @click="downloadImagesZip(selectedUser.id)">Download Images as Zip</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>


  

  
  <style scoped>
.cancel-button-top-right {
    position: absolute;
    top: 10px;
    right: 10px; /* Change this */
    background: none;
    border: none;
    color: rgb(255, 255, 255);
    font-size: 1.5em;
    cursor: pointer;
}

.user-image {
    width: 69px;
    height: 69px;
    object-fit: cover; /* Ensure the image covers the specified space without stretching */
}

.modal {
    position: fixed;
    z-index: 1;
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;
    overflow: auto;
    background-color: rgba(0,0,0,0.4);
}

.modal-content {
    position: relative;
    background-color: #292929;
    margin: 15% auto;
    padding: 20px;
    border: 1px solid #ff0000;
    width: 80%;
}

.scrollable {
    height: 400px; /* Adjust as needed */
    width: 100%;
    overflow-y: auto;
}

.image-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 10px;
}
</style>
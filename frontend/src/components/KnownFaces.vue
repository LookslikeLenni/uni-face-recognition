<!-- KnownFaces.vue -->
<script>
//note this is basically the same as AddingUnknownForm.vue
  export default {
    props: ['users'],
    data() {
      return {
        selectedUser: null,
        vieW: false,
        currentPage: 0,
        imagesPerPage: 69 
      };
    },
    /* mounted() {
      this.fetchUsers();

    }, */
    methods: {
        /* async fetchUsers() {
            try {
                const response = await fetch('http://127.0.0.1:8000/users');
                const data = await response.json();
                //console.log('Fetched users:', data);
                this.users = Array.isArray(data) ? data : [];
                //console.log('Users in component:', this.users);
            } catch (error) {
                console.error('Error fetching users:', error);
            }
        }, */
        getUserImageUrl(userId, imageIndex) {
            // Adjust the index based on the current page
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
        }
        ,
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

        },
    
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
      <h2>Identified:</h2>
        <div class="scrollable">
            <ul style="display: flex; flex-wrap: wrap; list-style: none;">
                <li
                    v-for="user in knownUsers"
                    :key="user.id"
                    style="flex: 0 0 200px; margin: 10px;"
                    >
                    <img :src="getUserImageUrl(user.id, 0)" alt="User Image" class="user-image" />
                    <div>
                        <p>{{ user.id }}</p>
                        <h3>{{ user.first_name }} {{ user.last_name }}</h3>
                        <p>{{ user.greeting }}</p>
                    </div>
                    <button class="delete" @click="deleteUser(user.id)">Delete</button>
                    <button class="selector" @click=selectUser(user)>Edit</button>
                    <button class="viewImages" @click="selectUser(user);vieW = true" >Images</button>
                </li>
            </ul>
        </div>
        <div v-if="selectedUser" class="modal">
            <div class="modal-content">
                <h2>Edit User</h2>
                <input v-model="selectedUser.first_name" placeholder="First Name">
                <input v-model="selectedUser.last_name" placeholder="Last Name">
                <input v-model="selectedUser.greeting" placeholder="Greeting">
                <button @click="updateUser">Save</button>
                <button @click="cancelEdit">Cancel</button>
            </div>
        </div>
        <div v-if="vieW&&selectedUser" class="modal">
            <div class="modal-content">
                <button @click="cancelEdit" class="cancel-button-top-right">✖</button> 
                <h2>View Images ({{ selectedUser.images.length }} total)</h2> 
                <ul class="image-grid">
                <li v-for="(image, index) in selectedUser.images.slice(currentPage * imagesPerPage, (currentPage + 1) * imagesPerPage)" :key="index">
                    <img :src="getUserImageUrl(selectedUser.id, index)" alt="User Image" class="user-image" />
                </li>
                </ul>
                <p>Page {{ currentPage + 1 }} of {{ Math.ceil(selectedUser.images.length / imagesPerPage) }}</p> 
                <button @click="prevPage">Previous Page</button> 
                <button @click="nextPage">Next Page</button> 
                <button @click="cancelEdit">Cancel</button>
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
    background-color: #777777;
    margin: 15% auto;
    padding: 20px;
    border: 1px solid #ff0000;
    width: 80%;
}

.scrollable {
    height: 400px; /* Adjust as needed */
    width: 500px;
    overflow-y: auto;
}

.image-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 10px;
}
</style>
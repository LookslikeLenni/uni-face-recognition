<template>
    <div>
      <h1>New Faces</h1>
        <div class="scrollable">
            <ul style="display: flex; flex-wrap: wrap; list-style: none;">
                <li
                v-for="user in newUsers"
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
                <button class="selector" @click=selectUser(user)>Add</button>
                <button class="merger" @click="this.merge=true; selectUser(user)">Merge</button>
                
                </li>
            </ul>
        </div>
        <div v-if="selectedUserToAddEditOrMerge" class="modal">
            <div class="modal-content">
                <h2>Edit User</h2>
                    <input v-model="selectedUserToAddEditOrMerge.first_name" placeholder="First Name">
                    <input v-model="selectedUserToAddEditOrMerge.last_name" placeholder="Last Name">
                    <input v-model="selectedUserToAddEditOrMerge.greeting" placeholder="Greeting">
                <button @click="updateUser">Save</button>
                <button @click="cancelEdit">Cancel</button>
            </div>
        </div>
        <div v-if="merge" class="modal">
            <div class="modal-content">
                <h2>Add Image to User</h2>
                <select v-model="selectedKnownUser">
                    <option disabled value="">Please select a known user</option>
                    <option v-for="user in knownUsers" :key="user.id" :value="user">{{ user.first_name }} {{ user.last_name }}</option>
                </select>
                <button @click="mergeImage(selectedKnownUser)">Merge</button>
                <button @click="cancelMerge">Cancel</button>
            </div>
        </div>
        <!-- mergeIamge function finish -->
    </div>
  </template>
  
  <script>
  //note this is basically the same as KnownFaces.vue
  export default {
    data() {
      return {
        users: [],
        selectedUserToAddEditOrMerge: null,
        selectedKnownUser: null,
        merge: false
      };
    },
    mounted() {
      this.fetchUsers();
    },
    methods: {
        async fetchUsers() {
            try {
                const response = await fetch('http://127.0.0.1:8000/users');
                const data = await response.json();
                //console.log('Fetched users:', data);
                this.users = Array.isArray(data) ? data : [];
                //console.log('Users in component:', this.users);
            } catch (error) {
                console.error('Error fetching users:', error);
            }
        },
        getUserImageUrl(userId, imageIndex) {
            return `http://127.0.0.1:8000/users/${userId}/images/${imageIndex}/`;
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
            this.selectedUserToAddEditOrMerge = {...user};
        },
        async updateUser() {
            try {
                console.log('Updating user:', this.selectedUserToAddEditOrMerge);
                let selectedUserID = this.selectedUserToAddEditOrMerge.id;
                const response = await fetch(`http://127.0.0.1:8000/users/${selectedUserID}/`, {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(this.selectedUserToAddEditOrMerge)
                });
                if (response.ok) {
                    this.fetchUsers();
                    this.selectedUserToAddEditOrMerge = null;
                } else {
                    console.error('Failed to update user');
                }
            } catch (error) {
                console.error('Error updating user:', error);
            }
        },
        cancelEdit() {
            this.selectedUserToAddEditOrMerge = null;
        },
        cancelMerge() {
            this.merge = false;
            this.selectedKnownUser = null;
        },
        async getFirstUserImage(userId) {
            try {
            const response = await fetch(`http://127.0.0.1:8000/users/${userId}/images/0/`);
            if (response.ok) {
                const blob = await response.blob();
                console.log('User image:', blob);
                return blob;
            } else {
                console.error('Failed to get user image');
            }
            } catch (error) {
            console.error('Error getting user image:', error);
            }
        },
        async mergeImage(selectedKnownUser) {
            if (!selectedKnownUser) {
                console.error('No known user selected');
            return;
            }
            try {
                let selectedUserToAddEditOrMergeID = this.selectedUserToAddEditOrMerge.id;
                const formData = new FormData();
                const blob = await this.getFirstUserImage(selectedUserToAddEditOrMergeID);
                formData.append('image_files', blob, 'image.jpg'); // 'image.jpg' is the filename, replace it with the actual filename if available

                console.log('Selected known user id:', selectedKnownUser.id);
                const response = await fetch(`http://127.0.0.1:8000/users/${selectedKnownUser.id}/images/`, {
                    method: 'POST',
                    body: formData
                });
                if (response.ok) {
                    console.log('Image added to user');
                    this.deleteUser(selectedUserToAddEditOrMergeID);
                    this.fetchUsers();
                    this.merge = false;
                } else {
                    console.error('Failed to add image to user');
                }
                } catch (error) {
                    console.error('Error adding image to user:', error);
            }
        }
    },
    computed: {
        newUsers() {
            return this.users.filter(user => user.first_name === 'Unknown');
        },
        knownUsers() {
            return this.users.filter(user => user.first_name !== 'Unknown');
        }
    }
  };
  </script>
  
  <style scoped>
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
    background-color: #777777;
    margin: 15% auto;
    padding: 20px;
    border: 1px solid #ff0000;
    width: 80%;
}

.scrollable {
    height: 400px; /* Adjust as needed */
    overflow-y: auto;
}
  </style>
  
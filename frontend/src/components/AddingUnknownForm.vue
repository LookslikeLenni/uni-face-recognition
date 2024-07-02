<script>
export default {
    //Tag: Sync
    props: ['users'],
    data() {
        return {
            selectedUserToAddEditOrMerge: null,
            selectedKnownUser: null,
            merge: false,
            currentlyMerging: false,
            listOfCheckedUserIds: [],
            mostSimilarUsers: {}, // Store the most similar users here
            similarityLoading: true,
        };
    },
    
    methods: {
        getUserImageUrl(userId, imageIndex) {
            return `http://127.0.0.1:8000/users/${userId}/images/${imageIndex}/`;
        },
        async deleteUser(userId, shouldConfirm = true) {
            if (shouldConfirm) {
                try {
                    const confirmed = confirm("Are you sure you want to delete this user?");
                    if (!confirmed) {
                        return;
                    }
                } catch (error) {
                    console.error('Error deleting user:', error);
                }
            }
            try {
                const response = await fetch(`http://127.0.0.1:8000/users/${userId}/`, {
                    method: 'DELETE'
                });
                if (response.ok) {
                    this.$emit('reload-components');
                    console.log('User deleted');
                } else {
                    console.error('Failed to delete user');
                }
            } catch (error) {
                console.error('Error deleting user:', error);
            }
        },
        selectUser(user) {
            this.selectedUserToAddEditOrMerge = { ...user };
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
                    this.$emit('reload-components');
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
            this.selectedUserToAddEditOrMerge = null;
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
            this.currentlyMerging = true;
            if (!selectedKnownUser) {
                console.error('No known user selected');
                return;
            }
            try {
                let selectedUserToAddEditOrMergeID = this.selectedUserToAddEditOrMerge.id;
                const formData = new FormData();
                const imageCount = this.selectedUserToAddEditOrMerge.images.length; // Use the length of the images array

                if (!imageCount) {
                    console.error('No images found for user');
                    return;
                }

                for (let i = 0; i < imageCount; i++) {
                    const imageUrl = this.getUserImageUrl(selectedUserToAddEditOrMergeID, i);
                    const response = await fetch(imageUrl);
                    const blob = await response.blob();
                    formData.append('image_files', blob, `image${i}.jpg`); // 'image.jpg' is the filename, replace it with the actual filename if available
                }

                console.log('Selected known user id:', selectedKnownUser.id);
                const response = await fetch(`http://127.0.0.1:8000/users/${selectedKnownUser.id}/images/`, {
                    method: 'POST',
                    body: formData
                });
                if (response.ok) {
                    console.log('Images added to user');
                    
                    await this.deleteUser(selectedUserToAddEditOrMergeID, false); //false = for not asking for confirmation pop up
                    this.$emit('reload-components');
                } else {
                    console.error('Failed to add images to user');
                }
            } catch (error) {
                console.error('Error adding images to user:', error);
            } finally {
                this.cancelMerge();
                this.cancelEdit();
                this.currentlyMerging = false;
            }
        },
        wasUserChecked(userId) {
            return this.listOfCheckedUserIds.includes(userId);
        },
        addUserIdToCheckedList(userId) {
            this.listOfCheckedUserIds.push(userId);
            //console.log('List of checked user ids:', this.listOfCheckedUserIds);
        },
        async compareAndGetMostSimilarUser(userId) {
            let mostSimilarUser = null;
            let highestSimilarity = 0;

            try {
                for (const user of this.knownUsers) {
                    if (user.id !== userId) {
                        const response = await fetch(`http://127.0.0.1:8000/compare/${userId}/${user.id}`);
                        if (response.ok) {
                            const data = await response.json();
                            if (data.similarity > highestSimilarity) {
                                highestSimilarity = data.similarity;
                                mostSimilarUser = user;
                            }
                        } else {
                            console.error(`Failed to compare users: ${response.statusText}`);
                        }
                    }
                }
            } catch (error) {
                console.error('Error comparing users:', error);
            }

            this.mostSimilarUsers[userId] = { user: mostSimilarUser, similarity: highestSimilarity.toFixed(2) };
            return mostSimilarUser;
        },
        async refreshSimilarityScores() {
            this.similarityLoading = true;
            await Promise.all(this.unknownUsers.map(user => this.compareAndGetMostSimilarUser(user.id)));
            this.similarityLoading = false;
        },
        async confirmUser(userId) {
            const similarUser = this.mostSimilarUsers[userId].user;
            this.selectedUserToAddEditOrMerge = this.unknownUsers.find(user => user.id === userId);
            await this.mergeImage(similarUser);
        }
    },
    computed: {
        unknownUsers() {
            return this.users.filter(user => user.first_name === 'Unknown');
        },
        knownUsers() {
            return this.users.filter(user => user.first_name !== 'Unknown');
        }
    },
    watch: {
        users: {
            immediate: true,
            handler() {
                this.refreshSimilarityScores();
            }
        }
    },
    async created() {
        await this.refreshSimilarityScores();
    }
};
</script>

<template>
    <div>
        <div class="scrollable">
            <ul class="d-flex flex-wrap list-unstyled">
                <li
                    v-for="user in unknownUsers"
                    :key="user.id"
                    class="m-2"
                    style="flex: 0 0 200px;"
                >
                    <img :src="getUserImageUrl(user.id, 0)" alt="User Image" class="user-image img-thumbnail" />
                    
                    <div v-if="wasUserChecked(user.id)">
                        <div>
                            <p>{{ user.id }}</p>
                            <h3>{{ user.first_name }} {{ user.last_name }}</h3>
                            <p>{{ user.greeting }}</p>
                        </div>
                        <button class="btn btn-outline-danger btn-sm" @click="deleteUser(user.id)">Delete</button>
                        <button class="btn btn-outline-primary btn-sm" @click="selectUser(user)">Add</button>
                        <button class="btn btn-outline-secondary btn-sm" @click="this.merge=true; selectUser(user)">Merge</button>    
                    </div>
                    <div v-else>
                        <p>{{ user.id }}</p>
                        <div v-if="similarityLoading">
                            <p>Loading...</p>
                        </div>
                        <div v-else-if="mostSimilarUsers[user.id]">
                            <p>Is this {{ mostSimilarUsers[user.id].user.first_name }}?</p>
                            <p>Similarity: {{ mostSimilarUsers[user.id].similarity }}</p>
                        </div>
                        <div v-else>
                            <p>No similar user found</p>
                        </div>
                        <button class="btn btn-outline-danger btn-sm" @click="addUserIdToCheckedList(user.id)">Wrong</button>
                        <button class="btn btn-outline-success btn-sm" @click="confirmUser(user.id)">Correct</button>
                    </div>
                </li>
            </ul>
            
        </div>
        <div v-if="selectedUserToAddEditOrMerge&&!merge&&!currentlyMerging" class="modal fade show" tabindex="-1" style="display: block;">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h2 class="modal-title">Edit User</h2>
                        <button type="button" class="btn-close" @click="cancelEdit"></button>
                    </div>
                    <div class="modal-body">
                        <input class="form-control mb-2" v-model="selectedUserToAddEditOrMerge.first_name" placeholder="First Name">
                        <input class="form-control mb-2" v-model="selectedUserToAddEditOrMerge.last_name" placeholder="Last Name">
                        <input class="form-control mb-2" v-model="selectedUserToAddEditOrMerge.greeting" placeholder="Greeting">
                    </div>
                    <div class="modal-footer">
                        <button class="btn btn-outline-success" @click="updateUser">Save</button>
                        <button class="btn btn-outline-secondary" @click="cancelEdit">Cancel</button>
                    </div>
                </div>
            </div>
        </div>
        <div v-if="merge&&!currentlyMerging" class="modal fade show" tabindex="-1" style="display: block;">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h3 class="modal-title">merge with User:</h3>
                        <button type="button" class="btn-close" @click="cancelMerge"></button>
                    </div>
                    <div class="modal-body">
                        <select class="form-select" v-model="selectedKnownUser">
                            <option disabled value="">Please select a known user</option>
                            <option v-for="user in knownUsers" :key="user.id" :value="user">{{ user.first_name }} {{ user.last_name }}</option>
                        </select>
                    </div>
                    <div class="modal-footer">
                        <button class="btn btn-outline-warning" @click="mergeImage(selectedKnownUser)">Merge</button>
                        <button class="btn btn-outline-secondary" @click="cancelMerge">Cancel</button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

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
background-color: #292929;
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
</style>

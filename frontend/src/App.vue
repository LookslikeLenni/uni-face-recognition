<script setup>
import { RouterLink, RouterView } from 'vue-router'

</script>

<template>
    <div class="container">
        <nav class="nav">
            <RouterLink to="/admin">Admin</RouterLink>|
            <RouterLink to="/">Home</RouterLink>|
            <RouterLink to="/statistics">Stats</RouterLink>
        </nav>
        <div class="content">
            <RouterView/>
        </div>
    </div>
</template>

<style scoped>
.container {
    display: flex;
    flex-direction: column;
    align-items: center;
    height: 100vh;
}

.nav {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    display: flex;
    justify-content: center;
    background: #252525;
}

.content {
	width: 100%; /* Add this line */
    margin-top: 50px; /* Adjust this value based on the height of your nav */
}
</style>

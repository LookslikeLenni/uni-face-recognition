<script setup>
import { RouterLink, RouterView } from 'vue-router'
import { ref, onMounted } from 'vue'
import feather from 'feather-icons'

const isDarkMode = ref(false)

function toggleDarkMode() {
    isDarkMode.value = !isDarkMode.value
    localStorage.setItem('isDarkMode', isDarkMode.value)
    applyDarkMode()
}

function applyDarkMode() {
    if (isDarkMode.value) {
        document.body.classList.add('bootstrap-dark')
    } else {
        document.body.classList.remove('bootstrap-dark')
    }
}

onMounted(() => {
    isDarkMode.value = localStorage.getItem('isDarkMode') === 'true'
    applyDarkMode()
    feather.replace() // Ensure icons are replaced on mount
})

function updateIcons() {
    feather.replace() // Ensure icons are updated after toggle
}
</script>

<template>
    <div :class="['container', { 'dark-mode': isDarkMode }]">
        <nav class="nav">
            <RouterLink to="/admin">Admin</RouterLink>|
            <RouterLink to="/">Home</RouterLink>|
            <RouterLink to="/statistics">Stats</RouterLink>
            <button @click="() => { toggleDarkMode(); updateIcons(); }">
                <i :data-feather="isDarkMode ? 'sun' : 'moon'"></i>
            </button>
        </nav>
        <div class="content">
            <RouterView/>
        </div>
    </div>
</template>

<style scoped>
.container {
    position: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
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
    width: 100%;
    margin-top: 50px;
}

button {
    margin-left: 20px;
    padding: 5px 10px;
    background: #444;
    color: #fff;
    border: none;
    cursor: pointer;
}

button:hover {
    background: #555;
}

button i {
    width: 24px;
    height: 24px;
    stroke: currentColor;
    fill: none;
    stroke-width: 2;
}

/* Add this section */
:global(.bootstrap-dark) {
    background-color: #121212;
    color: #e0e0e0;
}

:global(.bootstrap-dark .nav) {
    background: #333;
}

:global(.bootstrap-dark .button) {
    background: #444;
    color: #fff;
}

:global(.bootstrap-dark .button:hover) {
    background: #555;
}
</style>

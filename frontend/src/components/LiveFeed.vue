<script>
export default {
    data() {
        return {
            videoUrl: 'http://127.0.01:8000/video_feed'
        }
    },
}
//sollte des nicht mehr laufen ich hab den routerview aus dem div raus??
</script>

<template>
    <img class="video-feed" :src="videoUrl" alt="Live Feed" />
</template>

<style scoped>

.video-feed {
    border: 1px solid black;
    width: 900;
    height: auto;
}

</style>
<script>
export default {
    data() {
        return {
            videoUrl: 'http://127.0.0.1:8000/video_feed'
        }
    },
}
</script>

<template>
    <div class="container-lg">
        <img class="video-feed" :src="videoUrl" alt="Live Feed" />
    </div>
</template>

<style scoped>
.video-feed {
    width: 100%;
    height: auto;
    border: 2px solid #632c25; 
}

</style>

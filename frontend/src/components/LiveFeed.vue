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
    <div class="center-div">
        <img class="video-feed" :src="videoUrl" alt="Live Feed" />
    </div>
</template>

<style scoped>
/* .center-div {
    width: 100%;
    text-align: center;
}

.video-feed {
    width: 100%;
    height: auto;
    border: 1px solid #fff;
} */
</style>

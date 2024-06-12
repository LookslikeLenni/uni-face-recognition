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
    <div class="center-div">
        <img class="video-feed" :src="videoUrl" alt="Live Feed" />
    </div>
</template>

<style scoped>
.center-div {
    width: 100%;
    overflow: auto; /* or 'scroll' if you want to always show scrollbars */
    text-align: center; /* centers inline or inline-block elements */
}

.video-feed {
    display: inline-block;
    border: 1px solid rgb(255, 255, 255);
    width: 90%;
    height: auto;
}
</style>
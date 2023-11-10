<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router';

const laterVideo = ref(null)
laterVideo.value = JSON.parse(localStorage.getItem('save'))

const router = useRouter()
const goDetail = (video) => {
    // router.push(`/${video.id.videoId}`)
    router.push({
        name: 'videoDetail',
        params: {
            videoId: video.id.videoId
        }
    })
}

</script>

<template>
    <div>
        <h1>나중에 볼 동영상</h1>
        <div v-if="laterVideo">
            <div v-for="video in laterVideo" @click="goDetail(video)" class="product-card">
                <img :src="video.snippet.thumbnails.medium.url" alt="썸네일 이미지">
                {{ video.snippet.title }}
            </div>
        </div>
        <div v-else><p>등록된 비디오 없음</p></div>
    </div>
</template>

<style scoped>

</style>

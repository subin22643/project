<script setup>
import { ref, computed } from 'vue'
import { useRoute } from 'vue-router';
import axios from 'axios'
import router from '../router';

const route = useRoute()
const video = ref(null)
const videoId = route.params.videoId

const params = computed(() => ({
    part: 'snippet',
    id: videoId,
    key: 'AIzaSyBuy9d1EsPfUDFIdvSYxLvNd_iP23iqWQ0'
}))

const youtubeURL = 'https://www.googleapis.com/youtube/v3/videos'

const date = ref('')

axios.get(youtubeURL, { params: params.value } )
    .then((response) => {
        video.value = response.data.items[0]
        date.value = video.value.snippet.publishedAt
    }).catch((error) => {
        console.log(error)
    })


const videoURL = ref(`http://www.youtube.com/embed/${videoId}?enablejsapi=1`)


const saveButton = ref('동영상 저장')

const saveVideo = (video) => {

    const existing = JSON.parse(localStorage.getItem('save')) || []
    const isDuplicate = existing.length > 0 && existing.find((item) => item.id === video.id)

    if (!isDuplicate) {
        alert('동영상을 저장합니다')
        existing.push(video)
        saveButton.value = '저장 취소'
    } else {
        alert('저장된 동영상을 삭제합니다')
        existing.pop(video)
        saveButton.value = '동영상 저장'
    }

    localStorage.setItem('save', JSON.stringify(existing))
    router.push({ name: 'LaterView'})
}

const existingVideos = JSON.parse(localStorage.getItem('save')) || []
if (existingVideos.length > 0 && existingVideos.find((item) => item.id === videoId)) {
    saveButton.value = '저장 취소'
}

</script>

<template>
    <div>
        <nav>뒤로 가기</nav>
        <div v-if="video">
            <h1>{{ video.snippet.title }}</h1>
            <p>{{ video.snippet.description }}</p>
            <p>업로드 날짜: {{ date.slice(0,10) }}</p>
            <iframe id="player" type="text/html" width="720" height="480" :src="videoURL" frameborder="0"></iframe>
        </div>
        <div v-else>
            <p>로딩중입니다</p>
        </div>
        <button @click="saveVideo(video)">{{ saveButton }}</button>
    </div>
</template>

<style scoped>

</style>

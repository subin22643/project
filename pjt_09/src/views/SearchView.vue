<script setup>
import { ref, computed } from 'vue'
import { routerKey, useRouter } from 'vue-router'
import axios from 'axios'

const inputText = ref('')
const videos = ref([])
const youtubeURL = 'https://www.googleapis.com/youtube/v3/search'

const params = computed(() => ({
    part: 'snippet',
    q: inputText.value,
    regionCode : 'KR',
    type: 'video',
    maxResults: 3,
    key: 'AIzaSyBuy9d1EsPfUDFIdvSYxLvNd_iP23iqWQ0'
}))

const searchData = () => {
    params.value.q = inputText.value
    axios.get(youtubeURL, { params: params.value } )
    .then((response) => {
        videos.value = response.data.items
    }).catch((error) => {
        console.log(error)
    })
}

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


// const noVideo = computed(() => {
//     return videos.value.length > 0 ? true : false
// })

</script>

<template>
    <div>
        <h1>비디오 검색</h1>
        <form @submit.prevent="searchData">
            <input type="text" v-model="inputText">
            <button type="submit">찾기</button>
        </form> 
        <div class="product-list">
            <div v-for="video in videos" @click="goDetail(video)" class="product-card">
                <img :src="video.snippet.thumbnails.medium.url" alt="썸네일 이미지">
                {{ video.snippet.title }}
            </div>
        </div>
    </div>
</template>

<style scoped>

.product-list {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
}
.product-card {
    border: 1px solid black;
    width: 330px;
    text-align: center;

}
.product-card img {
    width: 320px;
    height: 180px;
    object-fit: fill;
}

</style>

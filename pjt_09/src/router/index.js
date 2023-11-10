import { createRouter, createWebHistory } from 'vue-router'
import SearchView from '../views/SearchView.vue'
import VideoDetailView from '../views/VideoDetailView.vue'
import LaterView from '../views/LaterView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/search',
      name: 'search',
      component: SearchView
    },
    {
      path: '/:videoId',
      name: 'videoDetail',
      component: VideoDetailView
    },
    {
      path: '/later',
      name: 'LaterView',
      component: LaterView
    }
  ]
})

export default router

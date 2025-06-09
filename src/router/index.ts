import { createRouter, createWebHistory } from 'vue-router'
import MainView from '@/views/MainView.vue'
import AddView from '@/views/AddView.vue'
import UploadView from '../views/UploadView.vue'
import DownloadView from '../views/DownloadView.vue'
import QueryView from '@/views/QueryView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: MainView,
    },
    {
      path: '/query',
      name: 'query',
      component: QueryView,
    },
    {
      path: '/add',
      name: 'add',
      component: AddView,
    },
    {
      path: '/upload',
      name: 'upload',
      component: UploadView,
    }
  ],
})

export default router

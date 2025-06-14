import { createRouter, createWebHistory } from 'vue-router'
import MainView from '@/views/MainView.vue'
import AddView from '@/views/AddView.vue'
import UploadView from '../views/UploadView.vue'
import QueryView from '@/views/QueryView.vue'
import ProfileView from '@/views/ProfileView.vue'

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
    },
    {
      path: '/profile',
      name: 'profile',
      component: ProfileView,
    },
  ],
})

export default router

// Add the following declaration to fix the TypeScript error
declare global {
  interface ImportMeta {
    env: {
      BASE_URL: string
      [key: string]: unknown
    }
  }
}

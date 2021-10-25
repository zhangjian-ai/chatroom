import Vue from 'vue'
import VueRouter from 'vue-router'

Vue.use(VueRouter)

const routes = [
  {
    path: '/chat_room',
    name: 'ChatRoom',
    component: () => import('../views/chatroom.vue'),
    meta: {
      title: "聊天室"
    }
  },
  {
    path: '/',
    name: 'Index',
    component: () => import('../views/index.vue'),
    meta: {
      title: "大厅"
    }
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router

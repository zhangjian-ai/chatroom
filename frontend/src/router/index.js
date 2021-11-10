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
    path: '/cars',
    name: 'Cars',
    component: () => import('../views/cars.vue'),
    meta: {
      title: "汽车之家-新闻"
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

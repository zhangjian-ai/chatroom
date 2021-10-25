import Vue from 'vue'
import Vuex from 'vuex'

import router from '@/router'

import { getConstance } from "@/api"

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    // 用户信息
    id: localStorage.id,
    nickname: localStorage.nickname,
    token: localStorage.token,

    status: localStorage.id > 0 ? true : false,

    // 常量信息
    constance: {},
  },
  mutations: {
    // 常量信息
    setConstance(state, payload) {
      if (payload) {
        state.constance.grade = payload.grade
      } else {
        state.constance = []
      }
    },

    // 设置用户信息
    setUserInfo(state, payload) {
      if (payload) {
        localStorage.token = payload.token;
        localStorage.id = payload.id;
        localStorage.nickname = payload.nickname;
      } else {
        localStorage.clear()
      }
      router.go(0)
    }

  },
  actions: {
    // 常量信息
    loadConstance(context) {
      getConstance().then(res => {
        context.commit("setConstance", res.data)
      })
    }
  },
  modules: {
  }
})

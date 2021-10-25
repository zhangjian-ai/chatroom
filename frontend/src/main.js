import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import vuetify from './plugins/vuetify'

import message from '@/components/Message'


// 安装 VueWechatTitle 组件库，用于动态展示网页title： npm install vue-wechat-title --save
import VueWechatTitle from "vue-wechat-title"

// 安装axios：npm install axios -S
import axios from "axios"



//环境的切换
if (process.env.NODE_ENV == 'development') {
    axios.defaults.baseURL = 'http://127.0.0.1:8000';
}
if (process.env.NODE_ENV == 'production') {
    axios.defaults.baseURL = 'http://:8000';
}

// 默认携带cookie发起请求和保存cookie
axios.defaults.withCredentials = true

// http request 拦截器
axios.interceptors.request.use(
    config => {
        if (store.state.token) {
            // 判断是否存在token，如果存在的话，则每个http header都加上token。本项目使用JWT
            config.headers.Authorization = `JWT ${store.state.token}`;
        }
        return config;
    },
    err => {
        return Promise.reject(err);
    });

// http response 拦截器
axios.interceptors.response.use(
    response => {
        return response;
    },
    error => {
        let res = error.response
        if (res) {
            switch (res.status) {
                case 401:
                    if (confirm("您的登录信息已过期，您可以取消以停留在此页，或点击确认重新登陆")) {
                        // 返回 401 清除token信息并跳转到登录页面
                        store.commit('setUserInfo');
                    }
                    break
                case 400:
                    message({
                        message: res.data.msg || '客户端错误',
                        type: 'error',
                    })
                    break;

                case 403:
                    message({
                        message: res.data.msg || '您的权限不足',
                        type: 'error',
                    })
                    break;

                case 404:
                    message({
                        message: res.data.msg || '网络请求不存在',
                        type: 'error',
                    })
                    break;

                case 500:
                    message({
                        message: res.data.msg || '服务器异常',
                        type: 'error',
                    })
                    break;

                case 501:
                    message({
                        message: res.data.msg || '您的操作被取消或不允许提交',
                        type: 'warning',
                    })
                    break;

                default:
                    message({
                        message: res.data.msg || '服务器正在开小差...',
                        type: 'error',
                    })
            }
        }
        // return Promise.reject(error.response.data)   // 返回接口返回的错误信息
        return Promise.reject(error.response)   // 返回接口返回的错误信息

    });

//  路由权限判断
router.beforeEach((to, from, next) => {
    if (to.meta.requireAuth) {  // 判断该路由是否需要登录权限
        if (store.state.token) {  // 通过vuex state获取当前的token是否存在
            next();
        }
        else {
            next({
                name: 'login_by_account',
                //   query: { redirect: to.fullPath }  // 将跳转的路由path作为参数，登录成功后跳转到该路由
            })
        }
    }
    else {
        next();
    }
})


Vue.config.productionTip = false

Vue.use(VueWechatTitle);
Vue.use(message);

new Vue({
    router,
    store,
    vuetify,
    render: h => h(App)
}).$mount('#app')

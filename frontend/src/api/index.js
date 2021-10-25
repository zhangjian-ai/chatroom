import axios from "axios"


// 获取系统配置常量
export const getConstance = () => { return axios.get("/const/detail/") }

// 注册
export const userLogon = data => { return axios.post("/users/logon/", data) }

// 登录
export const userLogin = data => { return axios.post("/users/login/", data) }
import axios from "axios"


// 获取系统配置常量
export const getConstance = () => { return axios.get("/const/detail/") }

// 注册
export const userLogon = data => { return axios.post("/users/logon/", data) }

// 登录
export const userLogin = data => { return axios.post("/users/login/", data) }

// 汽车之家 新闻查询
export const esNewsSearch = (content, tag, page, size) => { return axios.get("/es/news_search/", { params: { content: content, tag: tag, page: page, size: size } }) }
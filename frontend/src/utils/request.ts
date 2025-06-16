// src/utils/request.js
import axios from 'axios'

const request = axios.create({
  baseURL: 'http://47.111.154.156:5000/', // 默认请求地址
  timeout: 5000,
})
// 请求拦截器：自动添加 Token 到请求头
request.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('jwt_token')
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  },
)
export default request

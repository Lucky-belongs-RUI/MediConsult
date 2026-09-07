import axios from 'axios'
import type { AxiosInstance, AxiosRequestConfig } from 'axios'
import { ElMessage } from 'element-plus'

const service: AxiosInstance = axios.create({
  baseURL: import.meta.env.VITE_ALGO_URL,
  timeout: 60000
})

service.interceptors.request.use(
  (config) => {
    const userInfo = localStorage.getItem('userInfo')
    if (userInfo) {
      try {
        const { token } = JSON.parse(userInfo)
        if (token && config.headers) {
          config.headers.Authorization = `Bearer ${token}`
        }
      } catch {}
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

service.interceptors.response.use(
  (response) => {
    const { code, msg, data } = response.data

    if (code === 200) {
      return data
    }

    ElMessage.error(msg || '请求失败')
    return Promise.reject(new Error(msg || '请求失败'))
  },
  (error) => {
    ElMessage.error(error.message || '请求失败')
    return Promise.reject(error)
  }
)

const algoRequest = {
  get<T = any>(url: string, config?: AxiosRequestConfig): Promise<T> {
    return service.get(url, config)
  },

  post<T = any>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> {
    return service.post(url, data, config)
  },

  delete<T = any>(url: string, config?: AxiosRequestConfig): Promise<T> {
    return service.delete(url, config)
  },
}

export { algoRequest }

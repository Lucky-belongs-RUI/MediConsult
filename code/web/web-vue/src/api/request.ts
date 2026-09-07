import axios from 'axios'
import type { AxiosInstance, AxiosRequestConfig, InternalAxiosRequestConfig, AxiosResponse } from 'axios'
import { ElMessage } from 'element-plus'
import { useUserStore } from '@/stores/user'

const instance: AxiosInstance = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  timeout: 60000,
})

instance.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    const userInfo = localStorage.getItem('userInfo')
    if (userInfo) {
      const { token } = JSON.parse(userInfo)
      if (token && config.headers) {
        config.headers.Authorization = `Bearer ${token}`
      }
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

instance.interceptors.response.use(
  (response: AxiosResponse) => {
    if (response.config.responseType === 'blob') {
      return response.data
    }

    const { code, msg, data } = response.data

    if (code === 200 || code === 0) {
      return data
    }

    if (code === 401) {
      const userStore = useUserStore()
      userStore.logout(false)
      return Promise.reject(new Error('登录已过期，请重新登录'))
    }

    const error = new Error(msg || '请求失败') as Error & { response?: any }
    error.response = response
    ElMessage.error(msg || '请求失败')
    return Promise.reject(error)
  },
  (error) => {
    let message = '网络请求失败，请检查网络连接'
    if (error.response) {
      const { status, data } = error.response
      switch (status) {
        case 400:
          message = data.msg || '请求参数错误'
          break
        case 401:
          message = '登录已过期，请重新登录'
          const userStore = useUserStore()
          userStore.logout(false)
          break
        case 403:
          message = '没有权限访问该资源'
          break
        case 404:
          message = '请求的资源不存在'
          break
        case 500:
          message = '服务器内部错误'
          break
        default:
          message = data.msg || '请求失败'
      }
    }
    if (!error.config?.silent) {
      ElMessage.error(message)
    }
    return Promise.reject(error)
  }
)

const request = {
  get<T = any>(url: string, config?: AxiosRequestConfig): Promise<T> {
    return instance.get(url, config)
  },

  post<T = any>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> {
    return instance.post(url, data, config)
  },

  put<T = any>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> {
    return instance.put(url, data, config)
  },

  delete<T = any>(url: string, config?: AxiosRequestConfig): Promise<T> {
    return instance.delete(url, config)
  },
}

export { request }
 
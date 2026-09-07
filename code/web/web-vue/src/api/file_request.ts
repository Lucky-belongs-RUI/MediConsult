import axios from 'axios'
import type { AxiosInstance, AxiosRequestConfig, AxiosResponse } from 'axios'
import { ElMessage } from 'element-plus'

const service: AxiosInstance = axios.create({
  baseURL: import.meta.env.VITE_FILE_URL,
  timeout: 60000,
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
  (response: AxiosResponse) => {
    if (response.config.responseType === 'blob') {
      return response.data
    }

    const { code, msg, data } = response.data

    if (code === 200) {
      return data
    }

    ElMessage.error(msg || '请求失败')
    return Promise.reject(new Error(msg || '请求失败'))
  },
  (error) => {
    if (error.config?.responseType === 'blob' && error.response?.data) {
      return new Promise((_, reject) => {
        const reader = new FileReader()
        reader.onload = () => {
          try {
            const errorData = JSON.parse(reader.result as string)
            ElMessage.error(errorData.msg || '下载失败')
            reject(new Error(errorData.msg || '下载失败'))
          } catch (e) {
            ElMessage.error('下载失败')
            reject(new Error('下载失败'))
          }
        }
        reader.onerror = () => {
          ElMessage.error('下载失败')
          reject(new Error('下载失败'))
        }
        reader.readAsText(error.response.data)
      })
    }

    ElMessage.error(error.message || '请求失败')
    return Promise.reject(error)
  }
)

const fileRequest = {
  upload<T = { url: string, bucket: string, objectKey: string }>(bucket: string, file: File, isCache?: boolean, config?: AxiosRequestConfig): Promise<T> {
    const formData = new FormData()
    formData.append('file', file)
    if (isCache) {
      formData.append('is_cache', 'true')
    }
    return service.post(`/file/upload/${bucket}`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      ...config,
    })
  },

  get(bucket: string, objectKey: string, config?: AxiosRequestConfig): Promise<Blob> {
    return service.get(`/file/${bucket}/${objectKey}`, {
      responseType: 'blob',
      ...config,
    })
  },

  delete<T = any>(bucket: string, objectKey: string, config?: AxiosRequestConfig): Promise<T> {
    return service.delete(`/file/${bucket}/${objectKey}`, config)
  },

  getFileUrl(bucket: string, objectKey: string): string {
    return `${import.meta.env.VITE_FILE_URL}/file/${bucket}/${objectKey}`
  }
}

export { fileRequest }
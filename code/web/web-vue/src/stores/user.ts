import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { UserInfo, LoginResponse } from '@/types/user'
import { login as userLogin, logout as userLogout, updatePassword as updateUserPassword, register as userRegister } from '@/api/user'
import { ElMessage } from 'element-plus'
import router from '@/router'

export const useUserStore = defineStore('user', () => {
  const userInfo = ref<UserInfo | null>(null)
  const token = ref<string | null>(null)

  const initUserInfo = () => {
    const storedUserInfo = localStorage.getItem('userInfo')
    if (storedUserInfo) {
      try {
        const data = JSON.parse(storedUserInfo)
        userInfo.value = data.userInfo
        token.value = data.token
      } catch (error) {
        console.error('解析用户信息失败:', error)
        localStorage.removeItem('userInfo')
      }
    }
  }

  const login = async (username: string, password: string) => {
    try {
      const res = await userLogin(username, password)
      
      if (!res || !res.userInfo) {
        throw new Error('登录失败，请稍后重试')
      }
      userInfo.value = res.userInfo
      token.value = res.token || null
      localStorage.setItem('userInfo', JSON.stringify({
        userInfo: res.userInfo,
        token: res.token || null,
      }))
      ElMessage.success('登录成功')
      if (res.userInfo.role === 1) {
        router.push('/admin')
      } else {
        router.push('/user')
        console.log('登录成功-user')
      }
    } catch (error) {
      ElMessage.error('登录失败')
      throw error
    }
  }

  const logout = async (sendRequest: boolean = true) => {
    try {
      if (sendRequest) {
        try {
          await userLogout()
        } catch (error) {
          console.error('退出请求失败，但会继续清除本地登录状态')
        }
      }
      
      userInfo.value = null
      token.value = null
      localStorage.removeItem('userInfo')
      
      if (sendRequest) {
        ElMessage.success('退出成功')
      }
      
      router.push('/login')
    } catch (error) {
      userInfo.value = null
      token.value = null
      localStorage.removeItem('userInfo')
      router.push('/login')
      
      if (sendRequest) {
        ElMessage.error('退出失败')
        throw error
      }
    }
  }

  const isLoggedIn = () => {
    try {
      const storedUserInfo = localStorage.getItem('userInfo')
      if (!storedUserInfo) return false
      
      const data = JSON.parse(storedUserInfo)
      return !!(data.userInfo)
    } catch (error) {
      console.error('解析用户信息失败:', error)
      localStorage.removeItem('userInfo')
      return false
    }
  }

  const isAdmin = () => {
    try {
      const storedUserInfo = localStorage.getItem('userInfo')
      if (!storedUserInfo) return false
      
      const data = JSON.parse(storedUserInfo)
      return data.userInfo?.role === 1
    } catch (error) {
      console.error('解析用户信息失败:', error)
      localStorage.removeItem('userInfo')
      return false
    }
  }

  const changePassword = async (data: { id: number; oldPassword: string; newPassword: string }) => {
    await updateUserPassword(data)
  }

  const register = async (data: { username: string; password: string; realName: string; phone: string; email: string }) => {
    return userRegister(data)
  }

  return {
    userInfo,
    initUserInfo,
    login,
    logout,
    isLoggedIn,
    isAdmin,
    changePassword,
    register
  }
}) 
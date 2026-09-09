import { request } from './request'
import type { UserQueryParams, UserForm, UserInfo, LoginResponse } from '@/types/user'
import type { PageVO } from '@/types/common'
import type { UserVO } from '@/types/user'
export const userApi = {
  list: () => {
    return request.get<UserVO[]>('/user/list')
  }
}

export const login = async (username: string, password: string) => {
  const res = await request.post<LoginResponse>('/user/login', { username, password })
  return res
}

export const register = (data: {
  username: string
  password: string
  realName: string
  phone: string
  email: string
}) => {
  return request.post('/user/register', data)
}

export const logout = () => {
  return request.post('/user/logout')
}

export const updatePassword = (data: {
  id: number
  oldPassword: string
  newPassword: string
}) => {
  return request.post('/user/password', data)
}

export const getUserList = (params: UserQueryParams) => {
  return request.get<PageVO<UserInfo>>('/user/page', { params })
}

export const addUser = (data: UserForm) => {
  return request.post<void>('/user', data)
}

export const updateUser = (data: UserForm) => {
  return request.put<void>('/user', data)
}

export const deleteUser = (id: number) => {
  return request.delete<void>(`/user/${id}`)
}

export const resetPassword = (id: number) => {
  return request.put<void>(`/user/${id}/reset-password`)
}

export const updateUserStatus = (data: { id: number; status: number }) => {
  return request.put<void>(`/user/${data.id}/status`, { status: data.status })
}

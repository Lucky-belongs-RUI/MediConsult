export interface UserInfo {
  id: number
  username: string
  realName: string
  phone: string | null
  email: string | null
  role: number
  status: number
  avatarBucket?: string
  avatarObjectKey?: string
  avatarUrl?: string
  createTime?: string
  updateTime?: string
}
export interface UserVO {
  id: number
  username: string
  realName: string
}
export interface LoginResponse {
  userInfo: UserInfo
}

export enum UserRole {
  USER = 0,
  ADMIN = 1,
}

export enum UserStatus {
  DISABLED = 0,
  ENABLED = 1,
}

export interface UserListParams {
  page: number
  size: number
  username?: string
  realName?: string
  phone?: string
  email?: string
  role?: number
  status?: number
}

export interface UserListResult {
  total: number
  list: UserInfo[]
}

export interface AddUserParams {
  username: string
  password: string
  realName: string
  phone: string
  email: string
  role: number
  status: number
}

export interface UpdateUserParams {
  id: number
  username?: string
  realName?: string
  phone?: string
  email?: string
  role?: number
  status?: number
  avatarBucket?: string
  avatarObjectKey?: string
}

export interface UpdatePasswordParams {
  id: number
  oldPassword: string
  newPassword: string
}

export interface LoginParams {
  username: string
  password: string
}

export interface RegisterParams {
  username: string
  password: string
  realName: string
  phone: string
  email: string
}

export interface UserQueryParams {
  current: number
  size: number
  username?: string
  realName?: string
  phone?: string
  email?: string
  role?: number
  status?: number
}

export interface UserForm {
  id?: number
  username?: string
  password?: string
  realName?: string
  phone?: string
  email?: string
  role?: number
  status?: number
  avatarBucket?: string
  avatarObjectKey?: string
}
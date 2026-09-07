import type { UserInfo } from './user'

export interface CommentVO {
  id: number
  userId: number
  userInfo: UserInfo
  itemId: number
  content: string
  parentId?: number
  replyToCommentId?: number
  replyToUserId?: number
  replyToUserInfo?: UserInfo
  replies?: CommentVO[]
  createTime: string
  updateTime: string
}

export interface CommentAddDTO {
  userId?: number|undefined
  itemId: number
  content: string
  parentId?: number
  replyToCommentId?: number
  replyToUserId?: number
}

export interface CommentQueryDTO {
  itemId?: number
  userId?: number
  onlyParent?: boolean
  pageNo?: number
  pageSize?: number
} 
import { request } from './request'
import type { CommentAddDTO, CommentQueryDTO, CommentVO } from '@/types/comment'
import type { PageVO } from '@/types/common'

export const commentApi = {
  add: (data: CommentAddDTO) => {
    return request.post<number>('/comment', data)
  },

  delete: (commentId: number) => {
    return request.delete<boolean>(`/comment/${commentId}`)
  },

  get: (commentId: number) => {
    return request.get<CommentVO>(`/comment/${commentId}`)
  },

  page: (params: CommentQueryDTO) => {
    return request.get<PageVO<CommentVO>>('/comment/page', { params })
  },

  getTree: (itemId: number) => {
    return request.get<CommentVO[]>(`/comment/tree/${itemId}`)
  }
} 
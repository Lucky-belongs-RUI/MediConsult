import { request } from './request'
import type { LikeDTO } from '@/types/like'

export const likeApi = {
  like: (data: LikeDTO) => {
    return request.post('/like', data)
  },

  unlike: (itemId: number, userId?: number) => {
    return request.delete(`/like/${itemId}`, { params: { userId } })
  },

  status: (itemId: number,userId: number) => {
    return request.get<boolean>(`/like/status/${itemId}/${userId}`)
  },

  count: (itemId: number) => {
    return request.get<number>(`/like/count/${itemId}`)
  }
}

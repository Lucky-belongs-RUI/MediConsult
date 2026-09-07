import { request } from './request'
import type { LikeDTO, BatchLikeStatusResponse } from '@/types/like'

export const likeApi = {
  like: (data: LikeDTO) => {
    return request.post('/like', data)
  },

  unlike: (itemId: number) => {
    return request.delete(`/like/${itemId}`)
  },

  status: (itemId: number,userId: number) => {
    return request.get<boolean>(`/like/status/${itemId}/${userId}`)
  },

  count: (itemId: number) => {
    return request.get<number>(`/like/count/${itemId}`)
  },

  batchStatus: (itemIds: number[]) => {
    return request.get<BatchLikeStatusResponse>('/like/batch', {
      params: { itemIds }
    })
  },

  userLikedItems: () => {
    return request.get<number[]>('/like/user/items')
  }
} 
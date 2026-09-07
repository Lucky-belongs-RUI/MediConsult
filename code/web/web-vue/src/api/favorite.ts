import { request } from './request'
import type { FavoriteDTO, FavoriteVO } from '@/types/favorite'
import type { PageVO } from '@/types/common'

export const favoriteApi = {
  add: (data: FavoriteDTO) => {
    return request.post('/favorite', data)
  },

  remove: (itemId: number) => {
    return request.delete(`/favorite/${itemId}`)
  },

  status: (itemId: number,userId: number) => {
    return request.get<boolean>(`/favorite/status/${itemId}/${userId}`)
  },

  getUserFavoriteItemIds: (userId: number) => {
    return request.get<number[]>(`/favorite/user/items/${userId}`)
  },

  page: (userId: number,current: number = 1, size: number = 10) => {
    return request.get<PageVO<FavoriteVO>>('/favorite/user/page', {
      params: { userId,current, size }
    })
  },

  getItemFavoriteCount: (itemId: number) => {
    return request.get<number>(`/favorite/count/${itemId}`)
  }
} 
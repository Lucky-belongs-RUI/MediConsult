import { request } from './request'
import type { ItemAddDTO, ItemQueryDTO, ItemUpdateDTO, ItemVO } from '@/types/item'
import type { PageVO } from '@/types/common'

export const itemApi = {
  add: (data: ItemAddDTO) => {
    return request.post<number>('/item', data)
  },

  update: (data: ItemUpdateDTO) => {
    return request.put('/item', data)
  },

  delete: (id: number) => {
    return request.delete(`/item/${id}`)
  },

  getById: (id: number) => {
    return request.get<ItemVO>(`/item/${id}`)
  },

  page: (params: ItemQueryDTO) => {
    return request.get<PageVO<ItemVO>>('/item/page', { params })
  },

  listByCategoryId: (categoryId: number) => {
    return request.get<ItemVO[]>(`/item/list/category/${categoryId}`)
  }
}

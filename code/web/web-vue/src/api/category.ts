import { request } from './request'
import type { CategoryAddDTO, CategoryQueryDTO, CategoryUpdateDTO, CategoryVO } from '@/types/item'
import type { PageVO } from '@/types/common'

export const categoryApi = {
  add: (data: CategoryAddDTO) => {
    return request.post<number>('/category', data)
  },

  update: (data: CategoryUpdateDTO) => {
    return request.put('/category', data)
  },

  delete: (id: number) => {
    return request.delete(`/category/${id}`)
  },

  getById: (id: number) => {
    return request.get<CategoryVO>(`/category/${id}`)
  },

  list: () => {
    return request.get<CategoryVO[]>('/category/list')
  },

  page: (params: CategoryQueryDTO) => {
    return request.get<PageVO<CategoryVO>>('/category/page', { params })
  }
}
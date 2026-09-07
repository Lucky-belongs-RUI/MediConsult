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
  },

  listByTag: (tag: string) => {
    return request.get<ItemVO[]>(`/item/list/tag/${tag}`)
  },

  batchImport: (file: File) => {
    const formData = new FormData()
    formData.append('file', file)
    return request.post<{ successCount: number, failureCount: number, errors: string[] }>('/item/batch-import', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
  }
} 
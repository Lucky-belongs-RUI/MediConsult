import { request } from './request'
import type { PageVO } from '@/types/common'
import type { UserCase, UserCaseAddDTO, UserCaseUpdateDTO, UserCaseQueryParams } from '@/types/userCase'

export const userCaseApi = {
  /** 记录病例 */
  save(data: UserCaseAddDTO) {
    return request.post<number>('/user-case', data)
  },

  /** 我的病例（分页） */
  myPage(params: UserCaseQueryParams) {
    return request.get<PageVO<UserCase>>('/user-case/my', { params })
  },

  /** 病例详情 */
  getById(id: number) {
    return request.get<UserCase>(`/user-case/${id}`)
  },

  /** 更新病例 */
  update(data: UserCaseUpdateDTO) {
    return request.put('/user-case', data)
  },

  /** 公开 / 取消公开 */
  updateVisibility(id: number, isPublic: number) {
    return request.put('/user-case/visibility', { id, isPublic })
  },

  /** 删除病例 */
  delete(id: number) {
    return request.delete(`/user-case/${id}`)
  }
}

import { request } from '@/api/request'

export interface UserActionData {
  userId?: number | null;
  itemId: number;
  actionType: number;
  extraData?: string;
}

export interface UserActionQueryParams {
  current: number;
  size: number;
  userId?: number;
  itemId?: number;
  username?: string;
  itemTitle?: string;
  actionType?: number;
}

export interface UserActionResponse {
  records: any[];
  total: number;
  size: number;
  current: number;
  pages: number;
}

export function addUserAction(data: UserActionData): Promise<boolean> {
  return request.post('/user-action', data)
}

export function pageMyActions(params: UserActionQueryParams): Promise<UserActionResponse> {
  return request.get('/user-action/page', { params })
}

export function pageAllActions(params: UserActionQueryParams): Promise<UserActionResponse> {
  return request.get('/user-action/admin/page', { params })
}

export function batchDeleteActions(ids: number[]): Promise<boolean> {
  return request.delete('/user-action/batch', { data: ids })
}

export function batchDeleteMyActions(ids: number[]): Promise<boolean> {
  return request.delete('/user-action/my/batch', { data: ids })
}

export function getItemViewCount(itemId: number): Promise<number> {
  return request.get(`/user-action/view/count/${itemId}`)
}

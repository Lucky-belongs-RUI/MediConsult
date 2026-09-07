export interface PageDTO {
  current: number
  size: number
}

export interface PageVO<T> {
  records: T[]
  total: number
  size: number
  current: number
  pages: number
}

export interface Result<T> {
  code: number
  msg: string
  data: T
}
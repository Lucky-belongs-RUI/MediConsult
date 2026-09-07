export interface Category {
  id: number;
  name: string;
  iconUrl: string;
  iconObjectKey: string;
  iconBucket: string;
  description: string;
  createTime: string;
  updateTime: string;
}

export interface CategoryAddDTO {
  name: string;
  iconObjectKey: string;
  iconBucket: string;
  description: string;
}

export interface CategoryUpdateDTO {
  id: number;
  name?: string;
  iconObjectKey?: string;
  iconBucket?: string;
  description?: string;
}

export interface CategoryQueryDTO {
  name?: string;
  current?: number;
  size?: number;
}

export interface CategoryVO {
  id: number;
  name: string;
  iconUrl: string;
  iconObjectKey?: string;
  iconBucket?: string;
  description: string;
  createTime: string;
  updateTime: string;
}

export interface Item {
  id: number;
  title: string;
  description: string;
  coverUrl: string;
  coverObjectKey: string;
  coverBucket: string;
  fileUrl: string;
  fileObjectKey: string;
  fileBucket: string;
  tags: string;
  extraData?: string;
  categoryId: number;
  createTime: string;
  updateTime: string;
}

export interface ItemAddDTO {
  title: string;
  description: string;
  coverObjectKey: string;
  coverBucket: string;
  fileObjectKey: string;
  fileBucket: string;
  tags: string;
  extraData?: string;
  categoryId: number;
  userId: number;
}

export interface ItemUpdateDTO {
  userId: number;
  id: number;
  title?: string;
  description?: string;
  coverObjectKey?: string;
  coverBucket?: string;
  fileObjectKey?: string;
  fileBucket?: string;
  tags?: string;
  extraData?: string;
  categoryId?: number;
}

export interface ItemQueryDTO {
  title?: string;
  categoryId?: number;
  tag?: string;
  userRealName?: string;
  current?: number;
  size?: number;
}

export interface ItemVO {
  id: number;
  title: string;
  description: string;
  coverUrl: string;
  coverObjectKey?: string;
  coverBucket?: string;
  fileUrl: string;
  fileObjectKey?: string;
  fileBucket?: string;
  tags: string[];
  extraData?: string;
  category: CategoryVO;
  userId: number;
  userRealName?: string;
  createTime: string;
  updateTime: string;
  favorites?: number;
  views?: number;
} 
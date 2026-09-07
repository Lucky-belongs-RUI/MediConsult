import type { ItemVO } from './item'

export interface Favorite {
  id: number;
  userId: number;
  itemId: number;
  createTime: string;
}

export interface FavoriteDTO {
  itemId: number;
  userId: number|undefined;
}

export interface FavoriteStatusResponse {
  isFavorite: boolean;
}

export interface FavoriteVO {
  id: number;
  userId: number;
  itemId: number;
  item: ItemVO;
  createTime: string;
} 
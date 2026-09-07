export interface Like {
  id: number;
  userId: number;
  itemId: number;
  createTime: string;
}

export interface LikeDTO {
  userId: number|undefined;
  itemId: number;
}

export interface LikeStatusResponse {
  isLiked: boolean;
  count: number;
}

export interface BatchLikeStatusResponse {
  [itemId: number]: {
    isLiked: boolean;
    count: number;
  };
} 
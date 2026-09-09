export interface UserCase {
  id: number;
  userId: number;
  /** 公开后对应的病例库记录ID（item.id） */
  itemId?: number | null;
  title: string;
  patientName?: string;
  age?: number | null;
  gender?: string;
  categoryId?: number | null;
  remark?: string;
  content?: string;
  /** AI结构化摘要（模型按病例库格式输出的JSON） */
  aiSummary?: string;
  isPublic: number;
  createTime: string;
  updateTime: string;
  categoryName?: string;
  userRealName?: string;
}

export interface UserCaseAddDTO {
  userId: number;
  title: string;
  patientName?: string;
  age?: number | null;
  gender?: string;
  categoryId?: number | null;
  remark?: string;
  content?: string;
  aiSummary?: string;
  isPublic?: number;
}

export interface UserCaseUpdateDTO {
  id: number;
  title?: string;
  patientName?: string;
  age?: number | null;
  gender?: string;
  categoryId?: number | null;
  remark?: string;
  content?: string;
  isPublic?: number;
}

export interface UserCaseQueryParams {
  current: number;
  size: number;
  userId?: number;
  isPublic?: number;
  title?: string;
  categoryId?: number;
}

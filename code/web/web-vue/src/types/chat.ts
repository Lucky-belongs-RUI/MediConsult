export interface ChatModel {
  key: string;
  name: string;
}

export type ChatRole = 'user' | 'assistant';

export interface ChatMessage {
  id?: number;
  sessionId?: number;
  role: ChatRole;
  content: string;
  model?: string;
  extraData?: string;
  messageTime?: string;
}

export interface ChatSession {
  id: number;
  userId: number;
  sessionName: string;
  extraData?: string;
  createTime: string;
  updateTime: string;
  latestMessage?: string;
}

export interface ChatSessionCreateDTO {
  userId: number;
  sessionName: string;
  extraData?: string;
}

export interface ChatSessionUpdateDTO {
  id: number;
  sessionName: string;
}

export interface ChatMessageSendDTO {
  sessionId: number;
  content: string;
  model: string;
  extraData?: string;
}

export interface ChatMessageQueryDTO {
  sessionId: number;
}

/** 问诊基础信息（新建问诊时填写，随每次提问传给算法端作为 prompt 的一部分） */
export interface ConsultInfo {
  consultName: string;
  patientName: string;
  age: number | null;
  gender: string;
  categoryId: number | null;
  categoryName?: string;
  remark: string;
}
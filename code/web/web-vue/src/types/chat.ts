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
  createTime: string;
  updateTime: string;
  latestMessage?: string;
}

export interface ChatSessionCreateDTO {
  userId: number;
  sessionName: string;
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
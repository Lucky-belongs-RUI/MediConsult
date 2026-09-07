import { request } from './request'
import { algoRequest } from './algo_request'
import type { ChatSession, ChatMessage, ChatSessionCreateDTO, ChatSessionUpdateDTO, ChatMessageSendDTO, ChatMessageQueryDTO, ChatModel } from '@/types/chat'

export const chatApi = {
  getUserSessions(userId: number) {
    return request.get<ChatSession[]>(`/chat/user/${userId}`)
  },

  getSession(id: number) {
    return request.get<ChatSession>(`/chat/sessions/${id}`)
  },

  createSession(data: ChatSessionCreateDTO) {
    return request.post<ChatSession>('/chat/sessions', data)
  },

  updateSession(data: ChatSessionUpdateDTO) {
    return request.put<ChatSession>(`/chat/sessions/${data.id}`, data)
  },

  deleteSession(id: number) {
    return request.delete(`/chat/sessions/${id}`)
  },

  getMessages(params: ChatMessageQueryDTO) {
    return request.get<ChatMessage[]>('/chat/messages', { params })
  },

  sendMessage(data: ChatMessageSendDTO) {
    return request.post<ChatMessage>('/chat/messages', data)
  },

  clearSessionMessages(sessionId: number) {
    return request.delete(`/chat/sessions/${sessionId}/messages`)
  },

  deleteMessage(messageId: number) {
    return request.delete(`/chat/messages/${messageId}`)
  },

  updateMessageContent(messageId: number, content: string) {
    return request.put(`/chat/messages/${messageId}/content`, { content })
  }
}

export interface RAGResponse {
  response: string
  relevant_cases: Array<{
    id: number
    title: string
    description: string
    categoryName: string
    extraData?: Record<string, any>
  }>
  relevant_knowledge?: Array<{
    subject: string
    predicate: string
    object: string
    source: string
    category: string
  }>
  used_rag?: boolean
  used_knowledge_graph?: boolean
  rewritten_query?: string
}



export const llmApi = {
  getModels() {
    return algoRequest.get<ChatModel[]>('/llm/models')
  },

  chat(model: string, messages: ChatMessage[], enableRAG: boolean = false, enableKnowledgeGraph: boolean = false, imageInfo?: { bucket: string, objectKey: string }): Promise<RAGResponse> {
    const requestData: any = {
      model,
      messages: messages.map(msg => ({
        role: msg.role,
        content: msg.content
      })),
      enable_rag: enableRAG,
      enable_knowledge_graph: enableKnowledgeGraph
    }

    if (imageInfo) {
      requestData.image_info = {
        bucket: imageInfo.bucket,
        objectKey: imageInfo.objectKey
      }
    }

    return algoRequest.post<RAGResponse>('/llm/chat', requestData)
  },


} 
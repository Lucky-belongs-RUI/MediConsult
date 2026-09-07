import { algoRequest } from './algo_request'

export const documentApi = {
  generateCaseDocument(itemId: number) {
    return algoRequest.post<{
      downloadUrl: string;
      objectKey: string;
      fileName: string;
    }>('/document/generate-case-document', { itemId })
  },

  generateChatDocument(sessionId: number) {
    return algoRequest.post<{
      downloadUrl: string;
      objectKey: string;
      fileName: string;
      summary: Record<string, any>;
    }>('/document/generate-chat-document', { sessionId })
  }
} 
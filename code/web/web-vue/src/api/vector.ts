import { algoRequest } from './algo_request'

export interface VectorIndexInfo {
  exists: boolean
  count: number
  size: number
}

export interface KnowledgeGraphInfo {
  exists: boolean
  disease_count: number
  triple_count: number
}

export interface KnowledgeTriple {
  subject: string
  predicate: string
  object: string
  source: string
  category: string
}

export interface CaseMetadata {
  id: number
  title: string
  description: string
  categoryId: number
  categoryName: string
  tags: string
  extraData: Record<string, any> | null
  userId: number
  userName: string
  coverBucket: string
  coverObjectKey: string
  fileBucket: string
  fileObjectKey: string
  createTime: string
  updateTime: string
}

export interface UploadResponse {
  file_name: string
  file_path: string
  relative_path: string
}

export const vectorIndexApi = {
  getStatus: (): Promise<VectorIndexInfo> => {
    return algoRequest.get('/vector-index/status')
  },

  create: (): Promise<void> => {
    return algoRequest.post('/vector-index/create')
  },

  delete: (): Promise<void> => {
    return algoRequest.delete('/vector-index/delete')
  },

  update: async (): Promise<void> => {
    await vectorIndexApi.delete()
    await vectorIndexApi.create()
  },

  search: (query: string, topK?: number): Promise<CaseMetadata[]> => {
    return algoRequest.post('/vector-index/search', {
      query,
      top_k: topK || 5
    })
  }
}

export const knowledgeGraphApi = {
  getStatus: (): Promise<KnowledgeGraphInfo> => {
    return algoRequest.get('/knowledge-graph/status')
  },

  uploadFile: (file: File): Promise<UploadResponse> => {
    const formData = new FormData()
    formData.append('file', file)
    return algoRequest.post('/knowledge-graph/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
  },

  build: (filePath: string): Promise<any> => {
    return algoRequest.post('/knowledge-graph/build', { file_path: filePath })
  },

  delete: (): Promise<void> => {
    return algoRequest.delete('/knowledge-graph/delete')
  },

  search: (query: string, topK?: number, category?: string): Promise<KnowledgeTriple[]> => {
    return algoRequest.post('/knowledge-graph/search', {
      query,
      top_k: topK || 5,
      category
    })
  },

  getCategories: (): Promise<Array<{id: string, name: string, description: string}>> => {
    return algoRequest.get('/knowledge-graph/categories')
  }
}
import { algoRequest } from './algo_request'

export interface HealthResponse {
  status: string
  service: string
  version: string
}

export const checkAlgoHealth = () => {
  return algoRequest.get<HealthResponse>('/health/health_check')
} 
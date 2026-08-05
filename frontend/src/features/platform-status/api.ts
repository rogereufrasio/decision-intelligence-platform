import { apiRequest } from '../../lib/api/client'
import type { HealthResponse, ReadinessResponse } from '../../lib/api/types'

export const getHealth = () => apiRequest<HealthResponse>('/api/v1/health')
export const getReadiness = () => apiRequest<ReadinessResponse>('/api/v1/readiness')

import { apiRequest } from '../../lib/api/client'
import type { HealthResponse, ReadinessResponse } from '../../lib/api/types'

export const getSettingsHealth = () => apiRequest<HealthResponse>('/api/v1/health')
export const getSettingsReadiness = () => apiRequest<ReadinessResponse>('/api/v1/readiness')

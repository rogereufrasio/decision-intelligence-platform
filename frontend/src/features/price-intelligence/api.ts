import { apiRequest } from '../../lib/api/client'
import type { PriceIntelligenceResponse } from '../../types/history'

export const getPriceIntelligence = (searchId: string) => apiRequest<PriceIntelligenceResponse>(`/api/v1/price-intelligence/${encodeURIComponent(searchId)}?limit=20`)

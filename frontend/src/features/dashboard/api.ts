import { apiRequest } from '../../lib/api/client'
import type { MetricsResponse, SearchHistoryResponse } from '../../types/history'

export const getMetrics = () => apiRequest<MetricsResponse>('/api/v1/metrics')
export const getRecentSearches = () => apiRequest<SearchHistoryResponse>('/api/v1/search-history?limit=5')

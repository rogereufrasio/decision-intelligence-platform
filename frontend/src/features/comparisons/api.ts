import { apiRequest } from '../../lib/api/client'
import type { SearchComparisonResponse } from '../../types/comparison'
import type { SearchHistoryResponse } from '../../types/history'

export const getComparisonSnapshots = () => apiRequest<SearchHistoryResponse>('/api/v1/search-history?limit=100')

export const compareSnapshots = (baseSearchId: string, targetSearchId: string) => {
  const query = new URLSearchParams({ base_search_id: baseSearchId, target_search_id: targetSearchId })
  return apiRequest<SearchComparisonResponse>(`/api/v1/search-comparison?${query.toString()}`)
}

import { apiRequest } from '../../lib/api/client'
import type { SearchHistoryResponse, SearchSnapshot } from '../../types/history'

export const getSearchHistory = (limit: number) => apiRequest<SearchHistoryResponse>(`/api/v1/search-history?limit=${limit}`)
export const getSearchSnapshot = (searchId: string) => apiRequest<SearchSnapshot>(`/api/v1/search-history/${encodeURIComponent(searchId)}`)

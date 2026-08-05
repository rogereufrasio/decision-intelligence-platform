import { apiRequest } from '../../lib/api/client'
import type { SearchExportResponse } from '../../types/comparison'

export const exportSearchSnapshot = (searchId: string) => apiRequest<SearchExportResponse>(`/api/v1/search-history/${encodeURIComponent(searchId)}/export`)

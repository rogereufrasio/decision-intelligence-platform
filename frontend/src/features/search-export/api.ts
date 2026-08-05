import { apiRequestBlob } from '../../lib/api/client'

export const exportSearchSnapshot = (searchId: string) => apiRequestBlob(`/api/v1/search-history/${encodeURIComponent(searchId)}/export`)

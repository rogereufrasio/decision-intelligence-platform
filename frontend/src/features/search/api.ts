import { apiRequestWithMeta, type ApiResponse } from '../../lib/api/client'
import type { FlightSearchRequest, FlightSearchResponse } from '../../types/travel'

export function searchFlights(payload: FlightSearchRequest): Promise<ApiResponse<FlightSearchResponse>> {
  return apiRequestWithMeta('/api/v1/flights/search', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  })
}

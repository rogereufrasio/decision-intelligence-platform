import { apiRequestWithMeta, type ApiResponse } from '../../lib/api/client'
import type { FlightSearchRequest, FlightSearchResponse, TravelProvider } from '../../types/travel'

export function searchFlights(payload: FlightSearchRequest, provider: TravelProvider): Promise<ApiResponse<FlightSearchResponse>> {
  return apiRequestWithMeta('/api/v1/flights/search', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'X-Travel-Provider': provider },
    body: JSON.stringify(payload),
  })
}

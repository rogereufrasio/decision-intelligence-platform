import { apiRequestWithMeta, type ApiResponse } from '../../lib/api/client'
import type { PreferenceProfile, RecommendationOffer, RecommendationsResponse } from '../../types/travel'

export interface RecommendationRequest {
  offers: RecommendationOffer[]
  profile: PreferenceProfile
  preferred_providers: string[] | null
}

export function getRecommendations(
  payload: RecommendationRequest,
  correlationId: string | null,
): Promise<ApiResponse<RecommendationsResponse>> {
  return apiRequestWithMeta('/api/v1/recommendations', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
    correlationId: correlationId ?? undefined,
  })
}

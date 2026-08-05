export type PreferenceProfile = 'cheapest' | 'fastest' | 'balanced' | 'premium'

export interface SearchFormValues {
  origin: string
  destination: string
  departureDate: string
  returnDate: string
  adults: number
  profile: PreferenceProfile
  preferredProviders: string
}

export interface FlightSearchRequest {
  origin: string
  destination: string
  departure_date: string
  return_date: string | null
  passengers: number
  sort_by: 'cheapest' | 'fastest' | 'best_value'
}

export interface FlightOffer {
  id: string | null
  provider: string
  total_amount: string
  currency: string
  total_duration_minutes: number
  slices: Array<{ segments: unknown[] }>
}

export interface FlightSearchResponse {
  total_results: number
  applied_criterion: string
  offers: FlightOffer[]
}

export interface RecommendationOffer {
  provider: string
  product_type: 'flight'
  price: string
  currency: string
  metadata: null
  attributes: {
    total_duration_minutes: number
    stops: number
  }
}

export interface RecommendationScore {
  overall_score: string
  price_score: string
  duration_score: string
  provider_score: string
}

export interface RecommendationItem {
  offer: RecommendationOffer
  score: RecommendationScore
  rank: number
  profile: PreferenceProfile
  reasons: string[]
}

export interface RecommendationsResponse {
  best_recommendation: RecommendationItem | null
  recommendations: RecommendationItem[]
  total: number
}

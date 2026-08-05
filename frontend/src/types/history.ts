export interface MetricsResponse {
  total_requests: number
  requests_by_status: Record<string, number>
  total_errors: number
  average_response_time_ms: number
}

export interface SearchCriteria {
  origin: string
  destination: string
  departure_date: string
  return_date: string | null
  adults: number
}

export interface SearchOffer {
  provider: string
  product_type: string
  price: string
  currency: string
  metadata: Record<string, unknown> | null
  attributes: Record<string, unknown> | null
}

export interface SearchSnapshot {
  search_id: string
  criteria: SearchCriteria
  created_at: string
  provider: string
  status: string
  offers: SearchOffer[]
  sort_criterion: string | null
  schema_version: string
  correlation_id: string | null
  metadata: Record<string, unknown>
  warnings: string[]
}

export interface SearchHistoryResponse {
  items: SearchSnapshot[]
  total: number
}

export type PriceTrend = 'decreased' | 'increased' | 'stable' | 'insufficient_data'

export interface PriceIntelligenceResponse {
  current_price: string | null
  previous_price: string | null
  historical_min: string | null
  historical_max: string | null
  historical_average: string | null
  absolute_change: string | null
  percentage_change: string | null
  trend: PriceTrend
  snapshot_count: number
  currency: string | null
}

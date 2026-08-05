export interface SearchComparisonResponse {
  base_search_id: string
  target_search_id: string
  currency: string
  base_lowest_price: string
  target_lowest_price: string
  absolute_price_difference: string
  percentage_price_difference: string | null
  base_best_provider: string
  target_best_provider: string
  base_offer_count: number
  target_offer_count: number
  added_providers: string[]
  removed_providers: string[]
}

export interface SearchExportResponse { search_id: string; file: string; format: string }

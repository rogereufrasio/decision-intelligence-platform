import type { RecommendationItem, RecommendationOffer } from './travel'

export interface RejectedDecision {
  recommendation: RecommendationItem
  reasons: string[]
}

export interface DecisionExplanation {
  summary: string
  reasons: string[]
  warnings: string[]
  rejected_count: number
  profile: string
  selected_offer: RecommendationOffer | null
  selected_provider: string | null
  selected_price: string | null
  selected_currency: string | null
}

export interface DecisionSnapshot {
  decision_id: string
  search_id: string | null
  created_at: string
  profile: string
  accepted: RecommendationItem[]
  rejected: RejectedDecision[]
  explanation: DecisionExplanation
  selected_offer: RecommendationOffer | null
  schema_version: string
  correlation_id: string | null
}

export interface DecisionHistoryResponse { items: DecisionSnapshot[]; total: number }

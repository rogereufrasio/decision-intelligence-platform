import { apiRequest } from '../../lib/api/client'
import type { DecisionHistoryResponse } from '../../types/decision'

export const getDecisionHistory = () => apiRequest<DecisionHistoryResponse>('/api/v1/decision-history?limit=100')

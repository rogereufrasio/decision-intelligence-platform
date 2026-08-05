import { useState } from 'react'
import type { ApiResponse } from '../../lib/api/client'
import { getRecommendations } from '../recommendations/api'
import { searchFlights } from './api'
import { parsePreferredProviders, toRecommendationOffer, toSearchRequest } from './mappers'
import type { FlightSearchResponse, RecommendationsResponse, SearchFormValues } from '../../types/travel'
import { ApiError } from '../../lib/api/types'

interface SearchState {
  searchResult: FlightSearchResponse | null
  recommendations: RecommendationsResponse | null
  searchLoading: boolean
  recommendationLoading: boolean
  searchError: string | null
  recommendationError: string | null
  correlationId: string | null
}

const initialState: SearchState = {
  searchResult: null, recommendations: null, searchLoading: false,
  recommendationLoading: false, searchError: null, recommendationError: null,
  correlationId: null,
}

export function useTravelSearch() {
  const [state, setState] = useState<SearchState>(initialState)

  async function submit(values: SearchFormValues) {
    setState({ ...initialState, searchLoading: true })
    let searchResponse: ApiResponse<FlightSearchResponse>
    try {
      searchResponse = await searchFlights(toSearchRequest(values), values.travelProvider)
      setState((current) => ({ ...current, searchLoading: false, searchResult: searchResponse.data, correlationId: searchResponse.correlationId }))
    } catch (cause) {
      const suffix = cause instanceof ApiError && cause.correlationId ? ` Correlação: ${cause.correlationId}.` : ''
      const message = cause instanceof ApiError && cause.status > 0 ? cause.message : 'Não foi possível realizar a busca.'
      setState((current) => ({ ...current, searchLoading: false, searchError: `${message}${suffix}` }))
      return
    }

    if (!searchResponse.data.offers.length) return
    setState((current) => ({ ...current, recommendationLoading: true }))
    try {
      const response = await getRecommendations({
        offers: searchResponse.data.offers.map(toRecommendationOffer),
        profile: values.profile,
        preferred_providers: parsePreferredProviders(values.preferredProviders),
      }, searchResponse.correlationId)
      setState((current) => ({ ...current, recommendationLoading: false, recommendations: response.data, correlationId: response.correlationId ?? current.correlationId }))
    } catch {
      setState((current) => ({ ...current, recommendationLoading: false, recommendationError: 'As ofertas foram encontradas, mas não foi possível gerar recomendações.' }))
    }
  }

  return { ...state, submit }
}

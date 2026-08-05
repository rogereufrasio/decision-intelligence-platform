import { useCallback, useEffect, useState } from 'react'
import type { MetricsResponse, SearchHistoryResponse } from '../../types/history'
import { getMetrics, getRecentSearches } from './api'

interface Resource<T> { data: T | null; loading: boolean; error: string | null }
const empty = <T,>(): Resource<T> => ({ data: null, loading: true, error: null })

export function useDashboardData() {
  const [metrics, setMetrics] = useState<Resource<MetricsResponse>>(empty)
  const [recent, setRecent] = useState<Resource<SearchHistoryResponse>>(empty)

  const refresh = useCallback(() => {
    setMetrics({ data: null, loading: true, error: null })
    setRecent({ data: null, loading: true, error: null })
    getMetrics().then((data) => setMetrics({ data, loading: false, error: null })).catch(() => setMetrics({ data: null, loading: false, error: 'Métricas indisponíveis.' }))
    getRecentSearches().then((data) => setRecent({ data, loading: false, error: null })).catch(() => setRecent({ data: null, loading: false, error: 'Buscas recentes indisponíveis.' }))
  }, [])

  useEffect(refresh, [refresh])
  return { metrics, recent, refresh }
}

import { useCallback, useEffect, useState } from 'react'
import type { DecisionHistoryResponse, DecisionSnapshot } from '../../types/decision'
import { getDecisionHistory } from './api'

export function useDecisionHistory() {
  const [data, setData] = useState<DecisionHistoryResponse | null>(null)
  const [selected, setSelected] = useState<DecisionSnapshot | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const refresh = useCallback(() => {
    setLoading(true); setError(null)
    getDecisionHistory().then(setData).catch(() => setError('Histórico de decisões indisponível.')).finally(() => setLoading(false))
  }, [])
  useEffect(refresh, [refresh])
  return { data, selected, loading, error, refresh, select: setSelected }
}

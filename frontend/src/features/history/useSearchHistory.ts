import { useCallback, useEffect, useState } from 'react'
import type { SearchHistoryResponse, SearchSnapshot } from '../../types/history'
import { getSearchHistory, getSearchSnapshot } from './api'

export function useSearchHistory() {
  const [limit, setLimit] = useState(20)
  const [history, setHistory] = useState<SearchHistoryResponse | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [detail, setDetail] = useState<SearchSnapshot | null>(null)
  const [detailLoading, setDetailLoading] = useState(false)
  const [detailError, setDetailError] = useState<string | null>(null)

  const refresh = useCallback(() => {
    setLoading(true); setError(null)
    getSearchHistory(limit).then(setHistory).catch(() => setError('Histórico indisponível.')).finally(() => setLoading(false))
  }, [limit])
  useEffect(refresh, [refresh])

  async function select(searchId: string) {
    setDetailLoading(true); setDetailError(null); setDetail(null)
    try { setDetail(await getSearchSnapshot(searchId)) }
    catch { setDetailError('Não foi possível carregar os detalhes da busca.') }
    finally { setDetailLoading(false) }
  }

  return { limit, history, loading, error, detail, detailLoading, detailError, refresh, loadMore: () => setLimit((value) => Math.min(value + 20, 100)), select }
}

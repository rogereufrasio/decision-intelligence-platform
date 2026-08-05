import { useCallback, useEffect, useState } from 'react'
import { ApiError } from '../../lib/api/types'
import type { SearchComparisonResponse } from '../../types/comparison'
import type { SearchSnapshot } from '../../types/history'
import { compareSnapshots, getComparisonSnapshots } from './api'

function comparisonError(error: unknown) {
  if (error instanceof ApiError && error.status === 409) return 'As buscas selecionadas não possuem moeda comparável.'
  if (error instanceof ApiError && error.status === 404) return 'Um dos snapshots selecionados não foi encontrado.'
  if (error instanceof ApiError && error.status === 503) return 'A persistência de buscas está desabilitada.'
  return 'Não foi possível comparar as buscas.'
}

export function useComparison() {
  const [snapshots, setSnapshots] = useState<SearchSnapshot[]>([])
  const [selected, setSelected] = useState<string[]>([])
  const [result, setResult] = useState<SearchComparisonResponse | null>(null)
  const [loadingList, setLoadingList] = useState(true)
  const [loading, setLoading] = useState(false)
  const [listError, setListError] = useState<string | null>(null)
  const [error, setError] = useState<string | null>(null)
  const refresh = useCallback(() => {
    setLoadingList(true); setListError(null)
    getComparisonSnapshots().then((data) => setSnapshots(data.items)).catch(() => setListError('Histórico indisponível para comparação.')).finally(() => setLoadingList(false))
  }, [])
  useEffect(refresh, [refresh])
  function toggle(searchId: string) {
    setResult(null); setError(null)
    setSelected((current) => current.includes(searchId) ? current.filter((id) => id !== searchId) : current.length < 2 ? [...current, searchId] : [current[1]!, searchId])
  }
  async function compare() {
    if (selected.length !== 2 || selected[0] === selected[1]) return
    setLoading(true); setError(null)
    try { setResult(await compareSnapshots(selected[0]!, selected[1]!)) }
    catch (cause) { setResult(null); setError(comparisonError(cause)) }
    finally { setLoading(false) }
  }
  return { snapshots, selected, result, loadingList, loading, listError, error, refresh, toggle, compare, clear: () => { setSelected([]); setResult(null); setError(null) } }
}

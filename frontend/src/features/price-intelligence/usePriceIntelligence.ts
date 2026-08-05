import { useState } from 'react'
import type { PriceIntelligenceResponse } from '../../types/history'
import { getPriceIntelligence } from './api'

export function usePriceIntelligence() {
  const [data, setData] = useState<PriceIntelligenceResponse | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  async function load(searchId: string) {
    setLoading(true); setError(null); setData(null)
    try { setData(await getPriceIntelligence(searchId)) }
    catch { setError('Inteligência de preços indisponível.') }
    finally { setLoading(false) }
  }
  return { data, loading, error, load }
}

import { useRef, useState } from 'react'
import type { PriceIntelligenceResponse } from '../../types/history'
import { getPriceIntelligence } from './api'

export function usePriceIntelligence() {
  const selection = useRef(0)
  const [data, setData] = useState<PriceIntelligenceResponse | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  async function load(searchId: string) {
    const currentSelection = ++selection.current
    setLoading(true); setError(null); setData(null)
    try {
      const result = await getPriceIntelligence(searchId)
      if (currentSelection === selection.current) setData(result)
    }
    catch {
      if (currentSelection === selection.current) setError('Inteligência de preços indisponível.')
    }
    finally { if (currentSelection === selection.current) setLoading(false) }
  }
  return { data, loading, error, load }
}

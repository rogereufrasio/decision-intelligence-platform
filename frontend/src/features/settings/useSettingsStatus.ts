import { useEffect, useState } from 'react'
import type { HealthResponse, ReadinessResponse } from '../../lib/api/types'
import { getSettingsHealth, getSettingsReadiness } from './api'

export function useSettingsStatus() {
  const [health, setHealth] = useState<HealthResponse | null>(null)
  const [readiness, setReadiness] = useState<ReadinessResponse | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  useEffect(() => {
    Promise.all([getSettingsHealth(), getSettingsReadiness()]).then(([nextHealth, nextReadiness]) => { setHealth(nextHealth); setReadiness(nextReadiness) }).catch(() => setError('Não foi possível consultar o status operacional.')).finally(() => setLoading(false))
  }, [])
  return { health, readiness, loading, error }
}

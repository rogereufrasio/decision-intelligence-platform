import { useEffect, useState } from 'react'
import { getHealth, getReadiness } from './api'
import type { HealthResponse, ReadinessResponse } from '../../lib/api/types'

interface State {
  loading: boolean
  health: HealthResponse | null
  readiness: ReadinessResponse | null
  error: string | null
}

export function usePlatformStatus(): State {
  const [state, setState] = useState<State>({ loading: true, health: null, readiness: null, error: null })
  useEffect(() => {
    let active = true
    Promise.all([getHealth(), getReadiness()])
      .then(([health, readiness]) => active && setState({ loading: false, health, readiness, error: null }))
      .catch(() => active && setState({ loading: false, health: null, readiness: null, error: 'A API está indisponível no momento.' }))
    return () => { active = false }
  }, [])
  return state
}

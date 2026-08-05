import { ApiError, type ApiErrorPayload } from './types'

const DEFAULT_TIMEOUT_MS = 8_000
export const API_BASE_URL = (import.meta.env.VITE_API_BASE_URL ?? '').replace(/\/$/, '')

export interface ApiRequestOptions extends RequestInit {
  timeoutMs?: number
  correlationId?: string
}

function errorDetails(payload: ApiErrorPayload | null, fallback: string) {
  if (typeof payload?.detail === 'string') return { message: payload.detail, code: 'api_error' }
  if (payload?.detail && typeof payload.detail === 'object') {
    return { message: payload.detail.message ?? fallback, code: payload.detail.code ?? 'api_error' }
  }
  return { message: fallback, code: 'api_error' }
}

export async function apiRequest<T>(path: string, options: ApiRequestOptions = {}): Promise<T> {
  const { timeoutMs = DEFAULT_TIMEOUT_MS, correlationId, headers, ...requestOptions } = options
  const controller = new AbortController()
  const timeout = window.setTimeout(() => controller.abort(), timeoutMs)
  const requestHeaders = new Headers(headers)
  requestHeaders.set('Accept', 'application/json')
  if (correlationId) requestHeaders.set('X-Correlation-ID', correlationId)

  try {
    const response = await fetch(`${API_BASE_URL}${path}`, { ...requestOptions, headers: requestHeaders, signal: controller.signal })
    const responseCorrelationId = response.headers.get('X-Correlation-ID')
    const payload = response.status === 204 ? null : await response.json() as unknown
    if (!response.ok) {
      const details = errorDetails(payload as ApiErrorPayload | null, `A API respondeu com status ${response.status}.`)
      throw new ApiError(details.message, response.status, details.code, responseCorrelationId)
    }
    return payload as T
  } catch (error: unknown) {
    if (error instanceof ApiError) throw error
    if (error instanceof DOMException && error.name === 'AbortError') {
      throw new ApiError('A requisição excedeu o tempo limite.', 0, 'request_timeout', null)
    }
    throw new ApiError('Não foi possível conectar à API.', 0, 'network_error', null)
  } finally {
    window.clearTimeout(timeout)
  }
}

import { ApiError, type ApiErrorPayload } from './types'

const DEFAULT_TIMEOUT_MS = 8_000
export const API_BASE_URL = (import.meta.env.VITE_API_BASE_URL ?? '').replace(/\/$/, '')

export interface ApiRequestOptions extends RequestInit {
  timeoutMs?: number
  correlationId?: string
}

export interface ApiResponse<T> {
  data: T
  correlationId: string | null
}

export interface BlobResponse {
  blob: Blob
  fileName: string | null
  correlationId: string | null
}

function errorDetails(payload: ApiErrorPayload | null, fallback: string) {
  if (typeof payload?.detail === 'string') return { message: payload.detail, code: 'api_error' }
  if (payload?.detail && typeof payload.detail === 'object') {
    return { message: payload.detail.message ?? fallback, code: payload.detail.code ?? 'api_error' }
  }
  return { message: fallback, code: 'api_error' }
}

async function executeRequest(path: string, options: ApiRequestOptions): Promise<{ response: Response; correlationId: string | null }> {
  const { timeoutMs = DEFAULT_TIMEOUT_MS, correlationId, headers, ...requestOptions } = options
  const controller = new AbortController()
  const timeout = window.setTimeout(() => controller.abort(), timeoutMs)
  const requestHeaders = new Headers(headers)
  requestHeaders.set('Accept', 'application/json')
  if (correlationId) requestHeaders.set('X-Correlation-ID', correlationId)

  try {
    const response = await fetch(`${API_BASE_URL}${path}`, { ...requestOptions, headers: requestHeaders, signal: controller.signal })
    const responseCorrelationId = response.headers.get('X-Correlation-ID')
    if (!response.ok) {
      const payload = response.status === 204 ? null : await response.json() as unknown
      const details = errorDetails(payload as ApiErrorPayload | null, `A API respondeu com status ${response.status}.`)
      throw new ApiError(details.message, response.status, details.code, responseCorrelationId)
    }
    return { response, correlationId: responseCorrelationId }
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

export async function apiRequestWithMeta<T>(path: string, options: ApiRequestOptions = {}): Promise<ApiResponse<T>> {
  const result = await executeRequest(path, options)
  const payload = result.response.status === 204 ? null : await result.response.json() as unknown
  return { data: payload as T, correlationId: result.correlationId }
}

function contentDispositionFileName(value: string | null) {
  if (!value) return null
  const utf8 = value.match(/filename\*=UTF-8''([^;]+)/i)
  if (utf8?.[1]) return decodeURIComponent(utf8[1])
  return value.match(/filename="?([^";]+)"?/i)?.[1] ?? null
}

export async function apiRequestBlob(path: string, options: ApiRequestOptions = {}): Promise<BlobResponse> {
  const result = await executeRequest(path, options)
  return {
    blob: await result.response.blob(),
    fileName: contentDispositionFileName(result.response.headers.get('Content-Disposition')),
    correlationId: result.correlationId,
  }
}


export async function apiRequest<T>(path: string, options: ApiRequestOptions = {}): Promise<T> {
  return (await apiRequestWithMeta<T>(path, options)).data
}

import { describe, expect, test, vi } from 'vitest'
import { apiRequest } from '../lib/api/client'
import { jsonResponse } from './fixtures'

describe('apiRequest', () => {
  test('retorna JSON e envia correlation ID', async () => {
    const fetchMock = vi.fn().mockResolvedValue(jsonResponse({ ok: true })); vi.stubGlobal('fetch', fetchMock)
    await expect(apiRequest<{ ok: boolean }>('/ok', { correlationId: 'client-id' })).resolves.toEqual({ ok: true })
    const init = fetchMock.mock.calls[0]?.[1] as RequestInit
    expect(new Headers(init.headers).get('X-Correlation-ID')).toBe('client-id')
  })

  test('padroniza erro da API', async () => {
    vi.stubGlobal('fetch', vi.fn().mockResolvedValue(jsonResponse({ detail: { code: 'not_ready', message: 'Ainda não.' } }, 503)))
    await expect(apiRequest('/fail')).rejects.toMatchObject({ status: 503, code: 'not_ready', message: 'Ainda não.', correlationId: 'test-correlation' })
  })

  test('interrompe requisição por timeout', async () => {
    vi.stubGlobal('fetch', vi.fn((_url, init: RequestInit) => new Promise((_resolve, reject) => init.signal?.addEventListener('abort', () => reject(new DOMException('Aborted', 'AbortError'))))))
    await expect(apiRequest('/slow', { timeoutMs: 5 })).rejects.toMatchObject({ code: 'request_timeout' })
  })
})

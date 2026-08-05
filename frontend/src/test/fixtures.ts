export function jsonResponse(body: object, status = 200) {
  return new Response(JSON.stringify(body), { status, headers: { 'Content-Type': 'application/json', 'X-Correlation-ID': 'test-correlation' } })
}

export function platformFetch(input: RequestInfo | URL): Promise<Response> {
  const url = String(input)
  if (url.endsWith('/health')) return Promise.resolve(jsonResponse({ status: 'healthy', service: 'decision-intelligence-platform', version: '0.1.0' }))
  return Promise.resolve(jsonResponse({ status: 'ready', checks: [{ name: 'configuration', status: 'ready', message: 'Configuração carregada.' }] }))
}

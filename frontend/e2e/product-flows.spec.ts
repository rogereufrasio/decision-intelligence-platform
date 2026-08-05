import { expect, test } from '@playwright/test'

async function search(page: import('@playwright/test').Page) {
  await page.goto('/buscar')
  await page.getByLabel('Origem').fill('GIG')
  await page.getByLabel('Destino').fill('GRU')
  await page.getByLabel('Data de ida').fill('2026-09-10')
  await page.getByRole('button', { name: 'Buscar viagens' }).click()
  await expect(page.getByRole('heading', { name: 'Ofertas encontradas' })).toBeVisible()
  await expect(page.getByText('Melhor recomendação')).toBeVisible()
}

test('executa dashboard, preferência, busca, histórico, inteligência, comparação e exportação', async ({ page }) => {
  await page.goto('/')
  await expect(page.getByRole('heading', { name: 'Status da plataforma' })).toBeVisible()
  await expect(page.getByText('Disponível')).toBeVisible()
  await expect(page.getByText('Pronta')).toBeVisible()

  await page.goto('/configuracoes')
  await page.getByLabel('Provider padrão das buscas').selectOption('amadeus')
  await page.getByLabel('Provider padrão das buscas').selectOption('mock')
  const providerRequest = page.waitForRequest((request) => request.url().endsWith('/api/v1/flights/search'))
  await search(page)
  expect((await providerRequest).headers()['x-travel-provider']).toBe('mock')
  await expect(page.getByText('mock', { exact: true }).first()).toBeVisible()

  await search(page)
  await page.goto('/historico')
  await expect(page.getByText('GIG → GRU').first()).toBeVisible()
  await page.getByRole('button', { name: /GIG.*GRU/ }).first().click()
  await expect(page.getByRole('heading', { name: 'Detalhes da busca' })).toBeVisible()
  await expect(page.getByRole('heading', { name: 'Inteligência de preços' })).toBeVisible()

  const downloadPromise = page.waitForEvent('download')
  await page.getByRole('button', { name: 'Exportar Parquet' }).first().click()
  const download = await downloadPromise
  expect(download.suggestedFilename()).toMatch(/^search_.+\.parquet$/)

  await page.goto('/comparacoes')
  const choices = page.getByRole('checkbox')
  await expect(choices).toHaveCount(2)
  await choices.nth(0).check(); await choices.nth(1).check()
  await page.getByRole('button', { name: 'Comparar selecionadas' }).click()
  await expect(page.getByRole('heading', { name: 'Resultado da comparação' })).toBeVisible()
  await expect(page.getByText('Estável')).toBeVisible()
})

test('apresenta decisões vazias, IA controlada, navegação e 404', async ({ page, request }) => {
  await page.goto('/decisoes')
  await expect(page.getByText('Nenhuma decisão carregada')).toBeVisible()
  const aiResponse = await request.post('http://127.0.0.1:8000/api/v1/ai-explanations', { data: {} })
  expect(aiResponse.status()).toBe(422)
  await page.goto('/ia-assistiva')
  await expect(page.getByRole('heading', { name: 'IA assistiva' })).toBeVisible()
  await expect(page.getByText(/Nenhuma explicação é fabricada/)).toBeVisible()
  await page.goto('/rota-inexistente')
  await expect(page.getByRole('heading', { name: 'Página não encontrada' })).toBeVisible()
})

test('exibe estados reais para API indisponível e persistência 503', async ({ page }) => {
  await page.route('**/api/v1/health', (route) => route.abort())
  await page.goto('/')
  await expect(page.getByText('Serviço indisponível.')).toBeVisible()
  await page.unroute('**/api/v1/health')
  await page.route('**/api/v1/search-history?limit=100', (route) => route.fulfill({ status: 503, contentType: 'application/json', body: JSON.stringify({ detail: { code: 'search_persistence_disabled', message: 'disabled' } }), headers: { 'X-Correlation-ID': 'e2e-503' } }))
  await page.goto('/comparacoes')
  await expect(page.getByText('Histórico indisponível para comparação.')).toBeVisible()
})

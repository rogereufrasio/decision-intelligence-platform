import { execFileSync } from 'node:child_process'
import { resolve } from 'node:path'
import { expect, test, type Page } from '@playwright/test'

const api = 'http://127.0.0.1:8000/api/v1'
const backend = resolve('../backend')
const seedArgs = ['run', '--project', backend, 'python', '-m', 'tests.seed_functional_audit']

test.beforeEach(async ({ page }) => {
  const errors: string[] = []
  page.on('pageerror', error => errors.push(error.message))
  page.on('console', message => {
    if (message.type() === 'error' && !message.text().includes('Failed to load resource')) errors.push(message.text())
  })
  page.on('response', response => {
    if (response.status() >= 500) errors.push(`${response.status()} ${response.url()}`)
  })
  page.on('requestfailed', request => errors.push(`${request.url()} ${request.failure()?.errorText}`))
  // Checked after each test via a page-local collection, without intercepting traffic.
  observations.set(page, errors)
})
const observations = new WeakMap<Page, string[]>()
test.afterEach(async ({ page }, info) => {
  await info.attach('browser-observations', { body: JSON.stringify(observations.get(page)), contentType: 'application/json' })
  expect(observations.get(page)).toEqual([])
})

test('real search sequences preserve offer data through recommendation and history', async ({ page, request }, info) => {
  await page.goto('/buscar')
  await page.getByRole('button', { name: 'Buscar viagens' }).click()
  await expect(page.getByText('Informe a data de ida.')).toBeVisible()
  for (const [index, profile] of ['cheapest', 'fastest', 'balanced', 'premium'].entries()) {
    await page.getByLabel('Origem', { exact: true }).fill(index % 2 ? 'bsb' : 'gig')
    await page.getByLabel('Destino', { exact: true }).fill('gru')
    await page.getByLabel('Data de ida', { exact: true }).fill('2027-01-10')
    await page.getByLabel('Adultos', { exact: true }).fill(String(index + 1))
    await page.getByLabel('Perfil de preferência').selectOption(profile)
    const searchResponse = page.waitForResponse(r => r.url().endsWith('/flights/search'))
    const rankingResponse = page.waitForResponse(r => r.url().endsWith('/recommendations'))
    await page.getByRole('button', { name: 'Buscar viagens' }).click()
    const response = await searchResponse
    const result = await response.json()
    const ranking = await rankingResponse
    const recommendation = (await ranking.json()).best_recommendation
    await info.attach(profile, { body: JSON.stringify({ request: response.request().postDataJSON(), result, recommendation }), contentType: 'application/json' })
    expect(response.status()).toBe(200)
    expect(result.offers[0].total_amount).toBe('450.00')
    expect(result.offers[0].total_duration_minutes).toBe(120)
    expect(recommendation.offer.attributes.total_duration_minutes).toBe(120)
    expect(recommendation.profile).toBe(profile)
    expect(recommendation.rank).toBe(1)
    await expect(page.getByText('Duração: 2h 0min')).toBeVisible()
    const history = await (await request.get(`${api}/search-history?limit=1`)).json()
    expect(history.items[0].criteria.adults).toBe(index + 1)
    expect(history.items[0].offers[0].attributes.total_duration_minutes).toBe(result.offers[0].total_duration_minutes)
  }
  await page.getByLabel('Data de volta (opcional)').fill('2027-01-01')
  await page.getByRole('button', { name: 'Buscar viagens' }).click()
  await expect(page.getByText('A volta deve ser posterior à ida.')).toBeVisible()
  await page.getByLabel('Data de volta (opcional)').fill('2027-01-20')
  await page.getByRole('button', { name: 'Buscar viagens' }).click()
  await expect(page.getByText('Melhor recomendação')).toBeVisible()
})

test('persisted comparisons, pagination, price intelligence, decisions and valid Parquet', async ({ page, request }, info) => {
  execFileSync('uv', seedArgs, { cwd: backend })
  await page.goto('/comparacoes')
  const snapshots = (await (await request.get(`${api}/search-history?limit=100`)).json()).items
  const baseIndex = snapshots.findIndex((s: { search_id: string }) => s.search_id === 'audit-base')
  const targetIndex = snapshots.findIndex((s: { search_id: string }) => s.search_id === 'audit-target')
  await page.getByRole('checkbox').nth(baseIndex).check()
  await page.getByRole('checkbox').nth(targetIndex).check()
  const responsePromise = page.waitForResponse(r => r.url().includes('/search-comparison?'))
  await page.getByRole('button', { name: 'Comparar selecionadas' }).click()
  const comparison = await (await responsePromise).json()
  expect(comparison.absolute_price_difference).toBe('50')
  expect(Number(comparison.percentage_price_difference)).toBe(-10)
  await expect(page.getByText('Redução', { exact: true })).toBeVisible()
  await page.getByRole('button', { name: 'Limpar seleção' }).click()
  await expect(page.getByRole('heading', { name: 'Resultado da comparação' })).toHaveCount(0)
  await expect(page.getByRole('button', { name: 'Comparar selecionadas' })).toBeDisabled()

  await page.goto('/historico')
  await page.getByRole('button', { name: 'Carregar mais' }).click()
  await page.getByLabel('Filtrar por origem').fill('BSB')
  await expect(page.getByRole('button', { name: /Abrir detalhes/ })).toHaveCount(snapshots.filter((s: { criteria: { origin: string } }) => s.criteria.origin === 'BSB').length)
  await page.getByLabel('Filtrar por origem').fill('REC')
  await page.getByRole('button', { name: /Abrir detalhes/ }).click()
  await expect(page.getByText('Ainda não há dados suficientes', { exact: false })).toBeVisible()
  await page.getByLabel('Filtrar por origem').fill('ZZZ')
  await expect(page.getByText('Nenhum resultado', { exact: true })).toBeVisible()
  const price = await (await request.get(`${api}/price-intelligence/audit-target?limit=100`)).json()
  expect(price.snapshot_count).toBe(2)
  expect(Number(price.current_price)).toBe(450)
  expect(Number(price.previous_price)).toBe(500)
  expect(Number(price.historical_average)).toBe(475)
  expect(price.trend).toBe('decreased')

  await page.goto('/decisoes')
  await page.getByRole('button', { name: /audit-decision/ }).click()
  await expect(page.getByRole('heading', { name: 'Detalhes da decisão' })).toBeVisible()
  await expect(page.getByText('1 aceita(s)', { exact: true })).toBeVisible()
  const downloadPromise = page.waitForEvent('download')
  await page.getByRole('button', { name: 'Exportar Parquet' }).click()
  const download = await downloadPromise
  const file = info.outputPath('audit.parquet')
  await download.saveAs(file)
  const row = JSON.parse(execFileSync('uv', [...seedArgs, file], { cwd: backend, encoding: 'utf8' }))
  const snapshot = await (await request.get(`${api}/search-history/audit-target`)).json()
  expect(row.search_id).toBe(snapshot.search_id)
  expect(JSON.parse(row.offers_json)).toEqual(snapshot.offers)
  expect(JSON.parse(row.criteria_json)).toEqual(snapshot.criteria)
  await info.attach('parquet-decoded', { body: JSON.stringify(row), contentType: 'application/json' })
  await page.reload()
  await expect(page.getByRole('button', { name: /audit-decision/ })).toBeVisible()
})

test('API ranking oracles, invalid contracts, template AI and dashboard metrics', async ({ page, request }) => {
  const offers = [
    { provider: 'budget', price: '100', attributes: { total_duration_minutes: 300 } },
    { provider: 'quick', price: '300', attributes: { total_duration_minutes: 100 } },
    { provider: 'preferred', price: '200', attributes: { total_duration_minutes: 200 } },
  ].map(o => ({ ...o, currency: 'BRL', product_type: 'flight' }))
  for (const [profile, expected, score] of [['cheapest', 'budget', 70], ['fastest', 'quick', 70], ['balanced', 'preferred', 55], ['premium', 'preferred', 80]] as const) {
    const response = await request.post(`${api}/recommendations`, { data: { offers, profile, preferred_providers: ['preferred'] } })
    expect(response.status()).toBe(200)
    const body = await response.json()
    expect(body.best_recommendation.offer.provider).toBe(expected)
    expect(Number(body.best_recommendation.score.overall_score)).toBe(score)
    expect(body.recommendations.map((r: { rank: number }) => r.rank)).toEqual([1, 2, 3])
    expect(body.best_recommendation.reasons).toContain(profile === 'cheapest' ? 'Lowest price' : profile === 'fastest' ? 'Shortest duration' : 'Preferred provider')
  }
  expect((await (await request.post(`${api}/recommendations`, { data: { offers: [], profile: 'balanced' } })).json()).best_recommendation).toBeNull()
  for (const [path, status] of [['search-history?limit=0', 400], ['search-history?limit=101', 400], ['decision-history?limit=0', 422], ['price-intelligence/missing?limit=1', 422]] as const) expect((await request.get(`${api}/${path}`)).status()).toBe(status)
  for (const path of ['search-history/missing', 'search-history/missing/export', 'price-intelligence/missing', 'search-comparison?base_search_id=missing&target_search_id=missing']) expect((await request.get(`${api}/${path}`)).status()).toBe(404)
  const invalid = await request.post(`${api}/flights/search`, { data: { origin: '12!', destination: 'GRU', departure_date: 'bad', passengers: 0 } })
  expect(invalid.status()).toBe(400)
  const ai = await request.post(`${api}/ai-explanations`, { data: { context: { decision_explanation: { summary: 'Audit choice', reasons: ['Lowest price'], rejected_count: 0, profile: 'balanced' } } } })
  expect(ai.status()).toBe(200)
  expect((await ai.json()).summary).toBe('Audit choice')
  const metricsResponse = page.waitForResponse(r => r.url().endsWith('/metrics'))
  await page.goto('/')
  const metrics = await (await metricsResponse).json()
  const metricCard = page.getByText('Total de requests').locator('..')
  const displayedRequests = Number((await metricCard.textContent())?.match(/\d+/)?.[0])
  expect(displayedRequests).toBeGreaterThanOrEqual(metrics.total_requests)
  await page.getByRole('button', { name: 'Atualizar dashboard' }).click()
  await expect.poll(async () => Number((await metricCard.textContent())?.match(/\d+/)?.[0])).toBeGreaterThan(displayedRequests)
  await page.goto('/configuracoes')
  await page.getByLabel('Provider padrão das buscas').selectOption('duffel')
  await page.reload()
  await expect(page.getByLabel('Provider padrão das buscas')).toHaveValue('duffel')
  await page.goto('/buscar')
  await expect(page.getByLabel('Provider da busca')).toHaveValue('duffel')
  await page.getByLabel('Provider da busca').selectOption('mock')
  await page.setViewportSize({ width: 390, height: 844 })
  for (const path of ['/', '/buscar', '/historico', '/comparacoes', '/decisoes', '/configuracoes', '/ia-assistiva', '/missing']) {
    await page.goto(path)
    await expect(page.getByRole('main')).toBeVisible()
    expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth)).toBe(true)
  }
})

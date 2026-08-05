import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { beforeEach, expect, test, vi } from 'vitest'
import { SearchPage } from '../pages/SearchPage'

const mocks = vi.hoisted(() => ({
  searchFlights: vi.fn(),
  getRecommendations: vi.fn(),
}))

vi.mock('../features/search/api', () => ({ searchFlights: mocks.searchFlights }))
vi.mock('../features/recommendations/api', () => ({ getRecommendations: mocks.getRecommendations }))

const offer = {
  id: 'offer-1', provider: 'mock', total_amount: '450.00', currency: 'BRL',
  total_duration_minutes: 125, slices: [{ segments: [{}, {}] }],
}

const searchResponse = {
  data: { total_results: 1, applied_criterion: 'best_value', offers: [offer] },
  correlationId: 'search-correlation',
}

const recommendationResponse = {
  data: {
    total: 1,
    best_recommendation: {
      offer: { provider: 'mock', product_type: 'flight', price: '450.00', currency: 'BRL', metadata: null, attributes: { total_duration_minutes: 125, stops: 1 } },
      score: { overall_score: '92.5', price_score: '90', duration_score: '95', provider_score: '50' },
      rank: 1, profile: 'premium', reasons: ['Shortest duration'],
    },
    recommendations: [] as object[],
  },
  correlationId: 'recommendation-correlation',
}
recommendationResponse.data.recommendations = [recommendationResponse.data.best_recommendation]

async function completeForm(profile = 'premium') {
  const user = userEvent.setup()
  await user.type(screen.getByLabelText('Origem'), 'gig')
  await user.type(screen.getByLabelText('Destino'), 'gru')
  await user.type(screen.getByLabelText('Data de ida'), '2026-09-10')
  await user.type(screen.getByLabelText('Data de volta (opcional)'), '2026-09-20')
  await user.clear(screen.getByLabelText('Adultos'))
  await user.type(screen.getByLabelText('Adultos'), '2')
  await user.selectOptions(screen.getByLabelText('Perfil de preferência'), profile)
  await user.type(screen.getByLabelText(/Providers preferidos/), 'mock, amadeus')
  return user
}

beforeEach(() => {
  mocks.searchFlights.mockReset().mockResolvedValue(searchResponse)
  mocks.getRecommendations.mockReset().mockResolvedValue(recommendationResponse)
})

test('submete busca e perfil com payloads contratuais corretos', async () => {
  render(<SearchPage />); const user = await completeForm()
  await user.click(screen.getByRole('button', { name: 'Buscar viagens' }))

  await waitFor(() => expect(mocks.getRecommendations).toHaveBeenCalled())
  expect(mocks.searchFlights).toHaveBeenCalledWith({
    origin: 'GIG', destination: 'GRU', departure_date: '2026-09-10',
    return_date: '2026-09-20', passengers: 2, sort_by: 'best_value',
  }, 'mock')
  expect(mocks.getRecommendations).toHaveBeenCalledWith(
    expect.objectContaining({ profile: 'premium', preferred_providers: ['mock', 'amadeus'] }),
    'search-correlation',
  )
})

test('exibe loading enquanto busca está pendente', async () => {
  let resolveSearch: (value: typeof searchResponse) => void = () => undefined
  mocks.searchFlights.mockReturnValue(new Promise((resolve) => { resolveSearch = resolve }))
  render(<SearchPage />); const user = await completeForm('balanced')
  await user.click(screen.getByRole('button', { name: 'Buscar viagens' }))

  expect(screen.getByText('Buscando ofertas')).toBeInTheDocument()
  expect(screen.getByRole('button')).toBeDisabled()
  resolveSearch(searchResponse)
  await screen.findByText('Ofertas encontradas')
})

test('exibe oferta, melhor recomendação, scores e razões', async () => {
  render(<SearchPage />); const user = await completeForm()
  await user.click(screen.getByRole('button', { name: 'Buscar viagens' }))

  expect(await screen.findByText('Ofertas encontradas')).toBeInTheDocument()
  expect(screen.getAllByText('BRL 450.00')).toHaveLength(2)
  expect(screen.getByText('Duração: 2h 5min')).toBeInTheDocument()
  expect(screen.getByText('Melhor recomendação')).toBeInTheDocument()
  expect(screen.getByText(/Geral/)).toHaveTextContent('92.5')
  expect(screen.getByText('Shortest duration')).toBeInTheDocument()
  expect(screen.getByText('Referência: recommendation-correlation')).toBeInTheDocument()
})

test('exibe estado vazio e não solicita recomendações', async () => {
  mocks.searchFlights.mockResolvedValue({ data: { total_results: 0, applied_criterion: 'cheapest', offers: [] }, correlationId: 'empty' })
  render(<SearchPage />); const user = await completeForm('cheapest')
  await user.click(screen.getByRole('button', { name: 'Buscar viagens' }))

  expect(await screen.findByText('Nenhuma oferta encontrada')).toBeInTheDocument()
  expect(mocks.getRecommendations).not.toHaveBeenCalled()
})

test('separa erro de busca de erro de recomendação', async () => {
  mocks.searchFlights.mockRejectedValueOnce(new Error('offline'))
  render(<SearchPage />); let user = await completeForm()
  await user.click(screen.getByRole('button', { name: 'Buscar viagens' }))
  expect(await screen.findByText('Não foi possível realizar a busca.')).toBeInTheDocument()

  mocks.searchFlights.mockResolvedValue(searchResponse)
  mocks.getRecommendations.mockRejectedValueOnce(new Error('recommendation failed'))
  user = userEvent.setup()
  await user.click(screen.getByRole('button', { name: 'Buscar viagens' }))
  expect(await screen.findByText(/não foi possível gerar recomendações/)).toBeInTheDocument()
  expect(screen.getByText('Ofertas encontradas')).toBeInTheDocument()
})

test('permite realizar nova busca sem recarregar a página', async () => {
  render(<SearchPage />); const user = await completeForm('fastest')
  await user.click(screen.getByRole('button', { name: 'Buscar viagens' }))
  await screen.findByText('Melhor recomendação')
  await user.click(screen.getByRole('button', { name: 'Buscar viagens' }))
  await waitFor(() => expect(mocks.searchFlights).toHaveBeenCalledTimes(2))
})

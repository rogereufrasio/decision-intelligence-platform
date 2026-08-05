import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { beforeEach, expect, test, vi } from 'vitest'
import { HistoryPage } from '../pages/HistoryPage'

const mocks = vi.hoisted(() => ({ getSearchHistory: vi.fn(), getSearchSnapshot: vi.fn(), getPriceIntelligence: vi.fn() }))
vi.mock('../features/history/api', () => ({ getSearchHistory: mocks.getSearchHistory, getSearchSnapshot: mocks.getSearchSnapshot }))
vi.mock('../features/price-intelligence/api', () => ({ getPriceIntelligence: mocks.getPriceIntelligence }))

const offer = { provider: 'mock', product_type: 'flight', price: '1234.50', currency: 'BRL', metadata: null, attributes: { total_duration_minutes: 120 } }
const snapshot = {
  search_id: 'search-1', criteria: { origin: 'GIG', destination: 'GRU', departure_date: '2026-09-10', return_date: '2026-09-20', adults: 2 },
  created_at: '2026-08-05T12:00:00Z', provider: 'mock', status: 'completed', offers: [offer], sort_criterion: 'price',
  schema_version: '1.0', correlation_id: null, metadata: {}, warnings: ['Tarifa sujeita a alteração'],
}
const other = { ...snapshot, search_id: 'search-2', criteria: { ...snapshot.criteria, origin: 'BSB', destination: 'SSA' }, provider: 'amadeus' }
const price = {
  current_price: '1234.50', previous_price: '1300.00', historical_min: '1200.00', historical_max: '1400.00', historical_average: '1275.25',
  absolute_change: '-65.50', percentage_change: '-5.04', trend: 'decreased', snapshot_count: 4, currency: 'BRL',
}

beforeEach(() => {
  vi.clearAllMocks()
  mocks.getSearchHistory.mockResolvedValue({ items: [snapshot, other], total: 2 })
  mocks.getSearchSnapshot.mockResolvedValue(snapshot)
  mocks.getPriceIntelligence.mockResolvedValue(price)
})

test('exibe histórico vazio', async () => {
  mocks.getSearchHistory.mockResolvedValue({ items: [], total: 0 })
  render(<HistoryPage />)
  expect(await screen.findByText('Histórico vazio')).toBeInTheDocument()
})

test('lista histórico e formata datas em pt-BR', async () => {
  render(<HistoryPage />)
  expect(await screen.findByText(/GIG/)).toHaveTextContent('GIG → GRU')
  expect(screen.getAllByText('Ida: 10/09/2026')).toHaveLength(2)
  expect(screen.getAllByText(/05\/08\/2026/)).toHaveLength(2)
})

test('filtra por origem, destino, provider e status', async () => {
  render(<HistoryPage />); await screen.findByText(/GIG/)
  const user = userEvent.setup()
  await user.type(screen.getByLabelText('Filtrar por origem'), 'BSB')
  expect(screen.queryByText(/GIG/)).not.toBeInTheDocument(); expect(screen.getByText(/BSB/)).toBeInTheDocument()
  await user.type(screen.getByLabelText('Filtrar por destino'), 'SSA')
  await user.type(screen.getByLabelText('Filtrar por provider'), 'amadeus')
  await user.type(screen.getByLabelText('Filtrar por status'), 'completed')
  expect(screen.getByText(/BSB/)).toBeInTheDocument()
})

test('abre detalhes acessíveis e exibe ofertas, warnings e inteligência', async () => {
  render(<HistoryPage />); const user = userEvent.setup()
  await user.click(await screen.findByRole('button', { name: /GIG.*GRU/ }))
  expect(await screen.findByRole('heading', { name: 'Detalhes da busca' })).toBeInTheDocument()
  expect(screen.getAllByText(/1\.234,50/).length).toBeGreaterThan(0)
  expect(screen.getByText('Tarifa sujeita a alteração')).toBeInTheDocument()
  expect(await screen.findByRole('heading', { name: 'Inteligência de preços' })).toBeInTheDocument()
  expect(screen.getByText('Em queda')).toBeInTheDocument()
  expect(screen.getByText('-5,04%')).toBeInTheDocument()
  expect(mocks.getPriceIntelligence).toHaveBeenCalledWith('search-1')
})

test('informa dados insuficientes sem fabricar série temporal', async () => {
  mocks.getPriceIntelligence.mockResolvedValue({ ...price, current_price: null, previous_price: null, trend: 'insufficient_data', snapshot_count: 1 })
  render(<HistoryPage />); await userEvent.click(await screen.findByRole('button', { name: /GIG.*GRU/ }))
  expect(await screen.findByText(/Ainda não há dados suficientes/)).toBeInTheDocument()
  expect(screen.queryByRole('img')).not.toBeInTheDocument()
})

test('trata 503 do histórico e da inteligência separadamente', async () => {
  mocks.getSearchHistory.mockRejectedValueOnce(new Error('503'))
  const { unmount } = render(<HistoryPage />)
  expect(await screen.findByText('Histórico indisponível.')).toBeInTheDocument()
  unmount(); mocks.getSearchHistory.mockResolvedValue({ items: [snapshot], total: 1 }); mocks.getPriceIntelligence.mockRejectedValue(new Error('503'))
  render(<HistoryPage />); await userEvent.click(await screen.findByRole('button', { name: /GIG.*GRU/ }))
  expect(await screen.findByText('Inteligência de preços indisponível.')).toBeInTheDocument()
  expect(screen.getByRole('heading', { name: 'Detalhes da busca' })).toBeInTheDocument()
})

test('atualiza manualmente e amplia o limite local', async () => {
  mocks.getSearchHistory.mockResolvedValue({ items: [snapshot], total: 20 })
  render(<HistoryPage />); await screen.findByText(/GIG/)
  await userEvent.click(screen.getByRole('button', { name: 'Atualizar histórico' }))
  await waitFor(() => expect(mocks.getSearchHistory).toHaveBeenCalledTimes(2))
  await userEvent.click(screen.getByRole('button', { name: 'Carregar mais' }))
  await waitFor(() => expect(mocks.getSearchHistory).toHaveBeenLastCalledWith(40))
})

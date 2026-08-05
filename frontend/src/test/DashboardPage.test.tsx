import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { beforeEach, expect, test, vi } from 'vitest'
import { DashboardPage } from '../pages/DashboardPage'

const mocks = vi.hoisted(() => ({
  getHealth: vi.fn(), getReadiness: vi.fn(), getMetrics: vi.fn(), getRecentSearches: vi.fn(),
}))
vi.mock('../features/platform-status/api', () => ({ getHealth: mocks.getHealth, getReadiness: mocks.getReadiness }))
vi.mock('../features/dashboard/api', () => ({ getMetrics: mocks.getMetrics, getRecentSearches: mocks.getRecentSearches }))

const snapshot = {
  search_id: 'search-1', criteria: { origin: 'GIG', destination: 'GRU', departure_date: '2026-09-10', return_date: null, adults: 1 },
  created_at: '2026-08-05T12:00:00Z', provider: 'mock', status: 'completed', offers: [], sort_criterion: 'price',
  schema_version: '1.0', correlation_id: null, metadata: {}, warnings: [],
}

beforeEach(() => {
  vi.clearAllMocks()
  mocks.getHealth.mockResolvedValue({ status: 'healthy', service: 'DIP', version: '1.0' })
  mocks.getReadiness.mockResolvedValue({ status: 'ready', checks: [] })
  mocks.getMetrics.mockResolvedValue({ total_requests: 42, requests_by_status: { '200': 40 }, total_errors: 2, average_response_time_ms: 12.5 })
  mocks.getRecentSearches.mockResolvedValue({ items: [snapshot], total: 1 })
})

test('exibe métricas, status e buscas recentes', async () => {
  render(<DashboardPage />)
  expect(await screen.findByText('42')).toBeInTheDocument()
  expect(screen.getByText('12,5 ms')).toBeInTheDocument()
  expect(screen.getByText(/GIG/)).toHaveTextContent('GIG → GRU')
  expect(screen.getByRole('region', { name: 'Status da plataforma' })).toBeInTheDocument()
})

test('mantém buscas recentes quando métricas estão indisponíveis', async () => {
  mocks.getMetrics.mockRejectedValue(new Error('503'))
  render(<DashboardPage />)
  expect(await screen.findByText('Métricas indisponíveis.')).toBeInTheDocument()
  expect(screen.getByText(/GIG/)).toBeInTheDocument()
})

test('exibe estado vazio para buscas recentes', async () => {
  mocks.getRecentSearches.mockResolvedValue({ items: [], total: 0 })
  render(<DashboardPage />)
  expect(await screen.findByText('Nenhuma busca recente')).toBeInTheDocument()
})

test('atualiza manualmente as seções operacionais', async () => {
  render(<DashboardPage />)
  await screen.findByText('42')
  await userEvent.click(screen.getByRole('button', { name: 'Atualizar dashboard' }))
  await waitFor(() => expect(mocks.getMetrics).toHaveBeenCalledTimes(2))
  expect(mocks.getRecentSearches).toHaveBeenCalledTimes(2)
})

import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { beforeEach, expect, test, vi } from 'vitest'
import { DecisionsPage } from '../pages/DecisionsPage'

const mocks = vi.hoisted(() => ({ getDecisionHistory: vi.fn(), exportSearchSnapshot: vi.fn() }))
vi.mock('../features/decisions/api', () => ({ getDecisionHistory: mocks.getDecisionHistory }))
vi.mock('../features/search-export/api', () => ({ exportSearchSnapshot: mocks.exportSearchSnapshot }))

const offer = { provider: 'mock', product_type: 'flight' as const, price: '450.00', currency: 'BRL', metadata: null, attributes: { total_duration_minutes: 90, stops: 0 } }
const recommendation = { offer, score: { overall_score: '95', price_score: '100', duration_score: '90', provider_score: '50' }, rank: 1, profile: 'balanced' as const, reasons: ['Lowest price'] }
const decision = {
  decision_id: 'decision-1', search_id: 'search-1', created_at: '2026-08-05T12:00:00Z', profile: 'balanced', accepted: [recommendation],
  rejected: [{ recommendation: { ...recommendation, rank: 2 }, reasons: ['Price above limit'] }],
  explanation: { summary: 'Melhor opção selecionada.', reasons: ['Lowest price'], warnings: ['Uma opção foi rejeitada'], rejected_count: 1, profile: 'balanced', selected_offer: offer, selected_provider: 'mock', selected_price: '450.00', selected_currency: 'BRL' },
  selected_offer: offer, schema_version: '1.0', correlation_id: null,
}

beforeEach(() => { vi.clearAllMocks(); mocks.getDecisionHistory.mockResolvedValue({ items: [decision], total: 1 }) })

test('exibe histórico vazio de decisões', async () => {
  mocks.getDecisionHistory.mockResolvedValue({ items: [], total: 0 }); render(<DecisionsPage />)
  expect(await screen.findByText('Nenhuma decisão carregada')).toBeInTheDocument()
})

test('lista decisões com data, perfil, preço e contagens', async () => {
  render(<DecisionsPage />); expect(await screen.findByText('decision-1')).toBeInTheDocument()
  expect(screen.getByText('balanced')).toBeInTheDocument(); expect(screen.getByText(/R\$.*450,00/)).toBeInTheDocument()
  expect(screen.getByText('1 aceita(s) · 1 rejeitada(s)')).toBeInTheDocument(); expect(screen.getByText(/05\/08\/2026/)).toBeInTheDocument()
})

test('abre detalhe com explicação, reasons, warnings e recomendações', async () => {
  render(<DecisionsPage />); await userEvent.click(await screen.findByRole('button', { name: /decision-1/ }))
  expect(screen.getByRole('heading', { name: 'Detalhes da decisão' })).toBeInTheDocument()
  expect(screen.getByText('Melhor opção selecionada.')).toBeInTheDocument(); expect(screen.getByText('Lowest price')).toBeInTheDocument()
  expect(screen.getByText(/Uma opção foi rejeitada/)).toBeInTheDocument(); expect(screen.getByText(/Price above limit/)).toBeInTheDocument()
})

test('trata indisponibilidade e permite atualização manual', async () => {
  mocks.getDecisionHistory.mockRejectedValueOnce(new Error('503')); render(<DecisionsPage />)
  expect(await screen.findByText('Histórico de decisões indisponível.')).toBeInTheDocument()
  mocks.getDecisionHistory.mockResolvedValue({ items: [decision], total: 1 })
  await userEvent.click(screen.getByRole('button', { name: 'Atualizar decisões' }))
  await waitFor(() => expect(screen.getByText('decision-1')).toBeInTheDocument())
  expect(mocks.getDecisionHistory).toHaveBeenCalledTimes(2)
})

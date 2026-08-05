import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { beforeEach, expect, test, vi } from 'vitest'
import { ApiError } from '../lib/api/types'
import { ComparisonsPage } from '../pages/ComparisonsPage'

const mocks = vi.hoisted(() => ({ getComparisonSnapshots: vi.fn(), compareSnapshots: vi.fn(), exportSearchSnapshot: vi.fn() }))
vi.mock('../features/comparisons/api', () => ({ getComparisonSnapshots: mocks.getComparisonSnapshots, compareSnapshots: mocks.compareSnapshots }))
vi.mock('../features/search-export/api', () => ({ exportSearchSnapshot: mocks.exportSearchSnapshot }))

const makeSnapshot = (id: string, origin: string, destination: string) => ({
  search_id: id, criteria: { origin, destination, departure_date: '2026-09-10', return_date: null, adults: 1 },
  created_at: '2026-08-05T12:00:00Z', provider: id === 'base' ? 'mock' : 'amadeus', status: 'completed', offers: [],
  sort_criterion: 'price', schema_version: '1.0', correlation_id: null, metadata: {}, warnings: [],
})
const base = makeSnapshot('base', 'GIG', 'GRU'); const target = makeSnapshot('target', 'BSB', 'SSA')
const comparison = {
  base_search_id: 'base', target_search_id: 'target', currency: 'BRL', base_lowest_price: '500.00', target_lowest_price: '450.00',
  absolute_price_difference: '-50.00', percentage_price_difference: '-10.00', base_best_provider: 'mock', target_best_provider: 'amadeus',
  base_offer_count: 2, target_offer_count: 3, added_providers: ['amadeus'], removed_providers: ['mock'],
}

beforeEach(() => {
  vi.clearAllMocks(); mocks.getComparisonSnapshots.mockResolvedValue({ items: [base, target], total: 2 })
  mocks.compareSnapshots.mockResolvedValue(comparison)
  mocks.exportSearchSnapshot.mockResolvedValue({ blob: new Blob(['PAR1']), fileName: 'search_base.parquet', correlationId: null })
  vi.spyOn(HTMLAnchorElement.prototype, 'click').mockImplementation(() => undefined)
  vi.stubGlobal('URL', { ...URL, createObjectURL: vi.fn(() => 'blob:test'), revokeObjectURL: vi.fn() })
})

async function selectBoth() {
  const user = userEvent.setup(); render(<ComparisonsPage />)
  await user.click(await screen.findByLabelText(/GIG/)); await user.click(screen.getByLabelText(/BSB/)); return user
}

test('seleciona exatamente dois snapshots e envia a query contratual', async () => {
  const user = await selectBoth()
  expect(screen.getByText('2 de 2 snapshots selecionados.')).toBeInTheDocument()
  await user.click(screen.getByRole('button', { name: 'Comparar selecionadas' }))
  await waitFor(() => expect(mocks.compareSnapshots).toHaveBeenCalledWith('base', 'target'))
})

test('impede selecionar o mesmo snapshot duas vezes e desabilita comparação', async () => {
  const user = userEvent.setup(); render(<ComparisonsPage />)
  const checkbox = await screen.findByLabelText(/GIG/); await user.click(checkbox); await user.click(checkbox)
  expect(screen.getByRole('button', { name: 'Comparar selecionadas' })).toBeDisabled()
  expect(screen.queryByText(/snapshots selecionados/)).not.toBeInTheDocument()
})

test('exibe comparação negativa e providers adicionados e removidos', async () => {
  const user = await selectBoth(); await user.click(screen.getByRole('button', { name: 'Comparar selecionadas' }))
  expect(await screen.findByText('Redução')).toBeInTheDocument()
  expect(screen.getAllByText(/R\$.*50,00/).length).toBeGreaterThan(0)
  expect(screen.getByText('Providers adicionados').parentElement).toHaveTextContent('amadeus')
  expect(screen.getByText('Providers removidos').parentElement).toHaveTextContent('mock')
})

test('exibe comparação positiva', async () => {
  mocks.compareSnapshots.mockResolvedValue({ ...comparison, absolute_price_difference: '50.00', percentage_price_difference: '10.00' })
  const user = await selectBoth(); await user.click(screen.getByRole('button', { name: 'Comparar selecionadas' }))
  expect(await screen.findByText('Aumento')).toBeInTheDocument()
})

test.each([[409, 'As buscas selecionadas não possuem moeda comparável.'], [503, 'A persistência de buscas está desabilitada.'], [404, 'Um dos snapshots selecionados não foi encontrado.']])('trata erro %s de comparação', async (status, message) => {
  mocks.compareSnapshots.mockRejectedValue(new ApiError('erro', status, 'code', null))
  const user = await selectBoth(); await user.click(screen.getByRole('button', { name: 'Comparar selecionadas' }))
  expect(await screen.findByText(message)).toBeInTheDocument()
})

test('limpa a seleção e o resultado', async () => {
  const user = await selectBoth(); await user.click(screen.getByRole('button', { name: 'Limpar seleção' }))
  expect(screen.getByRole('button', { name: 'Comparar selecionadas' })).toBeDisabled()
})

test('inicia exportação com o nome retornado pela API', async () => {
  const user = userEvent.setup(); render(<ComparisonsPage />); await user.click(await screen.findByLabelText(/GIG/))
  await user.click(screen.getByRole('button', { name: 'Exportar Parquet' }))
  expect(await screen.findByText('Exportação preparada: search_base.parquet')).toBeInTheDocument()
  expect(mocks.exportSearchSnapshot).toHaveBeenCalledWith('base')
  expect(URL.revokeObjectURL).toHaveBeenCalledWith('blob:test')
})

test('não fabrica arquivo quando exportação falha', async () => {
  mocks.exportSearchSnapshot.mockRejectedValue(new Error('503')); const user = userEvent.setup(); render(<ComparisonsPage />)
  await user.click(await screen.findByLabelText(/GIG/)); await user.click(screen.getByRole('button', { name: 'Exportar Parquet' }))
  expect(await screen.findByText('Não foi possível exportar o snapshot.')).toBeInTheDocument()
  expect(HTMLAnchorElement.prototype.click).not.toHaveBeenCalled()
})

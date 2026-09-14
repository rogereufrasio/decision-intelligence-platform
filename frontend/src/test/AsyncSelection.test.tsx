import { act, renderHook, waitFor } from '@testing-library/react'
import { beforeEach, expect, test, vi } from 'vitest'
import { useComparison } from '../features/comparisons/useComparison'
import { useSearchHistory } from '../features/history/useSearchHistory'
import { usePriceIntelligence } from '../features/price-intelligence/usePriceIntelligence'

const mocks = vi.hoisted(() => ({
  compareSnapshots: vi.fn(),
  getSearchSnapshot: vi.fn(),
  getPriceIntelligence: vi.fn(),
}))

vi.mock('../features/comparisons/api', () => ({
  getComparisonSnapshots: async () => ({ items: [], total: 0 }),
  compareSnapshots: mocks.compareSnapshots,
}))
vi.mock('../features/history/api', () => ({
  getSearchHistory: async () => ({ items: [], total: 0 }),
  getSearchSnapshot: mocks.getSearchSnapshot,
}))
vi.mock('../features/price-intelligence/api', () => ({
  getPriceIntelligence: mocks.getPriceIntelligence,
}))

beforeEach(() => vi.clearAllMocks())

test('clearing selection invalidates a pending comparison', async () => {
  let resolve!: (value: object) => void
  mocks.compareSnapshots.mockReturnValue(new Promise((done) => { resolve = done }))
  const { result } = renderHook(useComparison)
  await waitFor(() => expect(result.current.loadingList).toBe(false))
  act(() => { result.current.toggle('A'); result.current.toggle('B') })
  let pending!: Promise<void>
  act(() => { pending = result.current.compare() })
  act(() => result.current.clear())

  await act(async () => {
    resolve({ base_search_id: 'A', target_search_id: 'B' })
    await pending
  })

  expect(result.current.selected).toEqual([])
  expect(result.current.result).toBeNull()
  expect(result.current.loading).toBe(false)
})

test('only the latest history selection can update the detail', async () => {
  let resolveA!: (value: object) => void
  mocks.getSearchSnapshot
    .mockReturnValueOnce(new Promise((done) => { resolveA = done }))
    .mockResolvedValueOnce({ search_id: 'B' })
  const { result } = renderHook(useSearchHistory)
  await waitFor(() => expect(result.current.loading).toBe(false))
  let pendingA!: Promise<void>
  act(() => { pendingA = result.current.select('A') })
  await act(async () => { await result.current.select('B') })
  await act(async () => { resolveA({ search_id: 'A' }); await pendingA })

  expect(result.current.detail?.search_id).toBe('B')
  expect(result.current.detailLoading).toBe(false)
})

test('only the latest price-intelligence selection can update the panel', async () => {
  let resolveA!: (value: object) => void
  mocks.getPriceIntelligence
    .mockReturnValueOnce(new Promise((done) => { resolveA = done }))
    .mockResolvedValueOnce({ current_price: '200' })
  const { result } = renderHook(usePriceIntelligence)
  let pendingA!: Promise<void>
  act(() => { pendingA = result.current.load('A') })
  await act(async () => { await result.current.load('B') })
  await act(async () => { resolveA({ current_price: '100' }); await pendingA })

  expect(result.current.data?.current_price).toBe('200')
  expect(result.current.loading).toBe(false)
})

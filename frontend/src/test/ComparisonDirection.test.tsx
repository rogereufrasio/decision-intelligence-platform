import { render, screen } from '@testing-library/react'
import { expect, test } from 'vitest'
import { ComparisonResult } from '../features/comparisons/ComparisonResult'

test('a positive absolute difference can represent a price reduction', () => {
  render(<ComparisonResult result={{
    base_search_id: 'base', target_search_id: 'target', currency: 'BRL',
    base_lowest_price: '500', target_lowest_price: '450',
    absolute_price_difference: '50', percentage_price_difference: '-10',
    base_best_provider: 'mock', target_best_provider: 'mock',
    base_offer_count: 1, target_offer_count: 1, added_providers: [], removed_providers: [],
  }} />)
  expect(screen.getByText('Redução')).toBeInTheDocument()
})

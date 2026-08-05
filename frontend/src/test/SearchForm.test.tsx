import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { vi } from 'vitest'
import { SearchForm } from '../features/search/SearchForm'

test('valida campos obrigatórios e não chama cliente com formulário inválido', async () => {
  const user = userEvent.setup()
  const onSubmit = vi.fn()
  render(<SearchForm onSubmit={onSubmit} loading={false} />)

  await user.click(screen.getByRole('button', { name: 'Buscar viagens' }))

  expect(screen.getAllByText('Informe um código IATA de 3 letras.')).toHaveLength(2)
  expect(screen.getByText('Informe a data de ida.')).toBeInTheDocument()
  expect(onSubmit).not.toHaveBeenCalled()
})

test('permite navegação por teclado e submissão válida', async () => {
  const user = userEvent.setup()
  const onSubmit = vi.fn().mockResolvedValue(undefined)
  render(<SearchForm onSubmit={onSubmit} loading={false} />)

  await user.tab()
  expect(screen.getByLabelText('Origem')).toHaveFocus()
  await user.type(screen.getByLabelText('Origem'), 'gig')
  await user.type(screen.getByLabelText('Destino'), 'gru')
  await user.type(screen.getByLabelText('Data de ida'), '2026-09-10')
  await user.click(screen.getByRole('button', { name: 'Buscar viagens' }))

  expect(onSubmit).toHaveBeenCalledWith(expect.objectContaining({
    origin: 'gig', destination: 'gru', departureDate: '2026-09-10', adults: 1,
  }))
})

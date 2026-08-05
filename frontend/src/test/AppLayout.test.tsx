import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { vi } from 'vitest'
import { App } from '../app/App'
import { platformFetch } from './fixtures'

beforeEach(() => { window.history.pushState({}, '', '/'); vi.stubGlobal('fetch', vi.fn(platformFetch)) })

test('renderiza layout com landmarks e navegação acessível', async () => {
  render(<App />)
  expect(screen.getByRole('banner')).toBeInTheDocument()
  expect(screen.getByRole('navigation', { name: 'Navegação principal' })).toBeInTheDocument()
  expect(screen.getByRole('main')).toBeInTheDocument()
  expect(await screen.findByText('Status da plataforma')).toBeInTheDocument()
})

test('navega entre páginas', async () => {
  const user = userEvent.setup(); render(<App />)
  await user.click(screen.getByRole('link', { name: 'Histórico' }))
  expect(screen.getByRole('heading', { name: 'Histórico' })).toBeInTheDocument()
  expect(screen.getByText('Nenhuma busca carregada')).toBeInTheDocument()
})

test('abre e fecha menu mobile', async () => {
  const user = userEvent.setup(); render(<App />)
  const button = screen.getByRole('button', { name: 'Abrir menu' })
  await user.click(button)
  expect(screen.getByRole('button', { name: 'Fechar menu' })).toHaveAttribute('aria-expanded', 'true')
  expect(screen.getAllByRole('navigation', { name: 'Navegação principal' })).toHaveLength(2)
})

test('exibe página 404', () => {
  window.history.pushState({}, '', '/nao-existe'); render(<App />)
  expect(screen.getByRole('heading', { name: 'Página não encontrada' })).toBeInTheDocument()
})

test('navega para o estado informativo de IA assistiva', async () => {
  const user = userEvent.setup(); render(<App />)
  await user.click(screen.getByRole('link', { name: 'IA assistiva' }))
  expect(screen.getByRole('heading', { name: 'IA assistiva' })).toBeInTheDocument()
  expect(screen.getByText(/Nenhuma explicação é fabricada/)).toBeInTheDocument()
})

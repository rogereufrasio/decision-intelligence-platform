import { render, screen } from '@testing-library/react'
import { vi } from 'vitest'
import { PlatformStatus } from '../features/platform-status/PlatformStatus'
import { platformFetch } from './fixtures'

test('exibe loading e depois health/readiness disponíveis', async () => {
  vi.stubGlobal('fetch', vi.fn(platformFetch)); render(<PlatformStatus />)
  expect(screen.getByRole('status')).toHaveTextContent('Verificando a plataforma')
  expect(await screen.findByText('Disponível')).toBeInTheDocument()
  expect(screen.getByText('Pronta')).toBeInTheDocument()
})

test('exibe estado indisponível quando API falha', async () => {
  vi.stubGlobal('fetch', vi.fn().mockRejectedValue(new TypeError('offline'))); render(<PlatformStatus />)
  expect(await screen.findByRole('alert')).toHaveTextContent('Serviço indisponível')
})

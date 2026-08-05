import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { beforeEach, expect, test, vi } from 'vitest'
import { SettingsPage } from '../pages/SettingsPage'

const mocks = vi.hoisted(() => ({ getSettingsHealth: vi.fn(), getSettingsReadiness: vi.fn() }))
vi.mock('../features/settings/api', () => ({ getSettingsHealth: mocks.getSettingsHealth, getSettingsReadiness: mocks.getSettingsReadiness }))

beforeEach(() => {
  mocks.getSettingsHealth.mockResolvedValue({ status: 'healthy', service: 'DIP', version: '1.1' })
  mocks.getSettingsReadiness.mockResolvedValue({ status: 'ready', checks: [] })
})

test('exibe status, providers suportados e orientação sobre credenciais', async () => {
  render(<SettingsPage />)
  expect(await screen.findByText('API: healthy')).toBeInTheDocument()
  expect(screen.getByLabelText('Provider padrão das buscas')).toHaveValue('mock')
  expect(screen.getByText(/nunca solicita nem armazena API keys/)).toBeInTheDocument()
})

test('salva e restaura somente a preferência local de provider', async () => {
  const user = userEvent.setup(); const first = render(<SettingsPage />)
  await screen.findByText('API: healthy')
  await user.selectOptions(screen.getByLabelText('Provider padrão das buscas'), 'duffel')
  expect(window.localStorage.getItem('dip.preferredTravelProvider')).toBe('duffel')
  expect(window.localStorage.length).toBe(1)
  first.unmount(); render(<SettingsPage />)
  expect(screen.getByLabelText('Provider padrão das buscas')).toHaveValue('duffel')
  await screen.findByText('API: healthy')
})

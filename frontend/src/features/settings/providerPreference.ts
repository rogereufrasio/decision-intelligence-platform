import type { TravelProvider } from '../../types/travel'

const STORAGE_KEY = 'dip.preferredTravelProvider'
const providers: TravelProvider[] = ['mock', 'amadeus', 'duffel']

export function getPreferredProvider(): TravelProvider {
  const value = window.localStorage.getItem(STORAGE_KEY)
  return providers.includes(value as TravelProvider) ? value as TravelProvider : 'mock'
}

export function savePreferredProvider(provider: TravelProvider) {
  window.localStorage.setItem(STORAGE_KEY, provider)
}

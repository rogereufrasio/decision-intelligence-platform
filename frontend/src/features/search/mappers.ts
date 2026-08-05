import type { FlightOffer, FlightSearchRequest, PreferenceProfile, RecommendationOffer, SearchFormValues } from '../../types/travel'

const sortByProfile: Record<PreferenceProfile, FlightSearchRequest['sort_by']> = {
  cheapest: 'cheapest',
  fastest: 'fastest',
  balanced: 'best_value',
  premium: 'best_value',
}

export function toSearchRequest(values: SearchFormValues): FlightSearchRequest {
  return {
    origin: values.origin.trim().toUpperCase(),
    destination: values.destination.trim().toUpperCase(),
    departure_date: values.departureDate,
    return_date: values.returnDate || null,
    passengers: values.adults,
    sort_by: sortByProfile[values.profile],
  }
}

export function toRecommendationOffer(offer: FlightOffer): RecommendationOffer {
  const segments = offer.slices.reduce((total, slice) => total + slice.segments.length, 0)
  return {
    provider: offer.provider,
    product_type: 'flight',
    price: offer.total_amount,
    currency: offer.currency,
    metadata: null,
    attributes: {
      total_duration_minutes: offer.total_duration_minutes,
      stops: Math.max(segments - offer.slices.length, 0),
    },
  }
}

export function parsePreferredProviders(value: string): string[] | null {
  const providers = value.split(',').map((provider) => provider.trim()).filter(Boolean)
  return providers.length ? providers : null
}

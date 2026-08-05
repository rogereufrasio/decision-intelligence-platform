import { Card } from '../../components/ui/Card'
import { EmptyState } from '../../components/ui/EmptyState'
import type { FlightSearchResponse } from '../../types/travel'

function duration(minutes: number) { const hours = Math.floor(minutes / 60); const rest = minutes % 60; return `${hours}h ${rest}min` }

export function SearchResults({ result }: { result: FlightSearchResponse }) {
  if (!result.offers.length) return <EmptyState title="Nenhuma oferta encontrada" description="Tente outras datas ou aeroportos." />
  return <section aria-labelledby="results-title"><div className="mb-3 flex items-end justify-between"><h2 id="results-title" className="text-xl font-semibold">Ofertas encontradas</h2><p className="text-sm text-slate-600">{result.total_results} oferta(s)</p></div><div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">{result.offers.map((offer, index) => <Card key={offer.id ?? `${offer.provider}-${index}`}><p className="text-sm font-semibold uppercase tracking-wide text-sky-700">{offer.provider}</p><p className="mt-3 text-2xl font-bold">{offer.currency} {offer.total_amount}</p>{offer.total_duration_minutes > 0 && <p className="mt-2 text-sm text-slate-600">Duração: {duration(offer.total_duration_minutes)}</p>}<p className="mt-2 text-sm text-slate-600">{offer.slices.length} trecho(s)</p></Card>)}</div></section>
}

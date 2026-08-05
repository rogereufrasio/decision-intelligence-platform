import { Alert } from '../../components/ui/Alert'
import { Card } from '../../components/ui/Card'
import { Loading } from '../../components/ui/Loading'
import type { SearchSnapshot } from '../../types/history'
import { formatCurrency, formatDate } from './formatters'

export function SnapshotDetail({ snapshot, loading, error }: { snapshot: SearchSnapshot | null; loading: boolean; error: string | null }) {
  if (loading) return <Loading label="Carregando detalhes" />
  if (error) return <Alert>{error}</Alert>
  if (!snapshot) return null
  return <section aria-labelledby="detail-title"><h2 id="detail-title" className="mb-3 text-xl font-semibold">Detalhes da busca</h2><Card><p className="font-semibold">{snapshot.criteria.origin} → {snapshot.criteria.destination}</p><p className="mt-1 text-sm text-slate-600">Criada em {formatDate(snapshot.created_at, true)} · {snapshot.criteria.adults} adulto(s)</p></Card><div className="mt-3 grid gap-3 md:grid-cols-2">{snapshot.offers.map((offer, index) => <Card key={`${offer.provider}-${index}`}><p className="font-semibold">{offer.provider}</p><p className="mt-2 text-xl font-bold">{formatCurrency(offer.price, offer.currency)}</p><p className="text-sm text-slate-600">{offer.product_type}</p></Card>)}</div>{snapshot.warnings.length > 0 && <Alert className="mt-3"><strong>Avisos:</strong><ul className="mt-1 list-disc pl-5">{snapshot.warnings.map((warning) => <li key={warning}>{warning}</li>)}</ul></Alert>}</section>
}

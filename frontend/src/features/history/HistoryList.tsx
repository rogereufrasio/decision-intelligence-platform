import { Badge } from '../../components/ui/Badge'
import { Button } from '../../components/ui/Button'
import { Card } from '../../components/ui/Card'
import { EmptyState } from '../../components/ui/EmptyState'
import type { SearchSnapshot } from '../../types/history'
import { formatDate } from './formatters'
import { ExportButton } from '../search-export/ExportButton'

export interface HistoryFilters { origin: string; destination: string; provider: string; status: string }

export function HistoryList({ items, filters, onFiltersChange, onSelect, onLoadMore, canLoadMore }: {
  items: SearchSnapshot[]; filters: HistoryFilters; onFiltersChange: (filters: HistoryFilters) => void;
  onSelect: (searchId: string) => void; onLoadMore: () => void; canLoadMore: boolean
}) {
  const filtered = items.filter((item) =>
    item.criteria.origin.toLowerCase().includes(filters.origin.toLowerCase()) &&
    item.criteria.destination.toLowerCase().includes(filters.destination.toLowerCase()) &&
    item.provider.toLowerCase().includes(filters.provider.toLowerCase()) &&
    item.status.toLowerCase().includes(filters.status.toLowerCase()))
  const field = (name: keyof HistoryFilters, label: string) => <label className="text-sm font-medium">{label}<input className="mt-1 w-full rounded-lg border border-slate-300 px-3 py-2" value={filters[name]} onChange={(event) => onFiltersChange({ ...filters, [name]: event.target.value })} /></label>
  return <section aria-labelledby="history-title"><h2 id="history-title" className="sr-only">Lista de buscas</h2><div className="mb-5 grid gap-3 sm:grid-cols-2 lg:grid-cols-4">{field('origin', 'Filtrar por origem')}{field('destination', 'Filtrar por destino')}{field('provider', 'Filtrar por provider')}{field('status', 'Filtrar por status')}</div>{filtered.length === 0 ? <EmptyState title="Nenhum resultado" description="Nenhuma busca corresponde aos filtros informados." /> : <div className="space-y-3">{filtered.map((item) => <Card key={item.search_id}><button type="button" onClick={() => onSelect(item.search_id)} className="w-full rounded-lg text-left"><div className="flex flex-wrap items-center gap-2"><strong>{item.criteria.origin} → {item.criteria.destination}</strong><Badge>{item.status}</Badge><span className="ml-auto text-xs text-slate-500">{formatDate(item.created_at, true)}</span></div><div className="mt-3 grid gap-1 text-sm text-slate-600 sm:grid-cols-2 lg:grid-cols-4"><span>Ida: {formatDate(item.criteria.departure_date)}</span><span>Volta: {formatDate(item.criteria.return_date)}</span><span>{item.provider}</span><span>{item.offers.length} oferta(s) · {item.sort_criterion ?? 'sem critério'}</span></div><span className="mt-2 block text-xs font-semibold text-sky-700">Abrir detalhes</span></button><div className="mt-3"><ExportButton searchId={item.search_id} /></div></Card>)}</div>}{canLoadMore && <div className="mt-4"><Button variant="secondary" onClick={onLoadMore}>Carregar mais</Button></div>}</section>
}

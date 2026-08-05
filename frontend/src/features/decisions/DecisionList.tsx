import { Badge } from '../../components/ui/Badge'
import { Card } from '../../components/ui/Card'
import type { DecisionSnapshot } from '../../types/decision'
import { formatCurrency, formatDate } from '../history/formatters'

export function DecisionList({ items, onSelect }: { items: DecisionSnapshot[]; onSelect: (item: DecisionSnapshot) => void }) {
  return <section aria-labelledby="decision-list"><h2 id="decision-list" className="sr-only">Lista de decisões</h2><div className="space-y-3">{items.map((item) => <Card key={item.decision_id}><button type="button" className="w-full rounded-lg text-left" onClick={() => onSelect(item)}><div className="flex flex-wrap gap-2"><strong>{item.decision_id}</strong><Badge>{item.profile}</Badge><span className="ml-auto text-xs text-slate-500">{formatDate(item.created_at, true)}</span></div><div className="mt-2 grid gap-1 text-sm text-slate-600 sm:grid-cols-3"><span>Busca: {item.search_id ?? 'não vinculada'}</span><span>{item.explanation.selected_provider ?? 'Sem provider'} · {formatCurrency(item.explanation.selected_price, item.explanation.selected_currency)}</span><span>{item.accepted.length} aceita(s) · {item.rejected.length} rejeitada(s)</span></div><span className="mt-2 block text-xs font-semibold text-sky-700">Abrir decisão</span></button></Card>)}</div></section>
}

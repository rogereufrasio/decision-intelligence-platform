import { Alert } from '../../components/ui/Alert'
import { Card } from '../../components/ui/Card'
import type { DecisionSnapshot } from '../../types/decision'
import { formatCurrency } from '../history/formatters'

export function DecisionDetail({ item }: { item: DecisionSnapshot | null }) {
  if (!item) return null
  return <section aria-labelledby="decision-detail" className="space-y-3"><h2 id="decision-detail" className="text-xl font-semibold">Detalhes da decisão</h2><Card><p className="font-semibold">{item.explanation.summary}</p><p className="mt-2">Selecionada: {item.selected_offer?.provider ?? 'Nenhuma'} · {formatCurrency(item.selected_offer?.price ?? null, item.selected_offer?.currency ?? null)}</p></Card><div className="grid gap-3 md:grid-cols-2"><Card><h3 className="font-semibold">Razões</h3><ul className="mt-2 list-disc pl-5">{item.explanation.reasons.map((reason) => <li key={reason}>{reason}</li>)}</ul></Card><Card><h3 className="font-semibold">Recomendações</h3><p>{item.accepted.length} aceita(s)</p><p>{item.rejected.length} rejeitada(s)</p>{item.accepted.map((entry) => <p key={`${entry.rank}-${entry.offer.provider}`}>#{entry.rank} {entry.offer.provider}</p>)}{item.rejected.map((entry) => <p key={`${entry.recommendation.rank}-${entry.recommendation.offer.provider}`}>{entry.recommendation.offer.provider}: {entry.reasons.join(', ')}</p>)}</Card></div>{item.explanation.warnings.length > 0 && <Alert><strong>Avisos:</strong> {item.explanation.warnings.join(' · ')}</Alert>}</section>
}

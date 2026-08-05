import { Badge } from '../../components/ui/Badge'
import { Card } from '../../components/ui/Card'
import type { RecommendationsResponse } from '../../types/travel'

export function RecommendationResults({ result }: { result: RecommendationsResponse }) {
  if (!result.recommendations.length) return null
  const bestRank = result.best_recommendation?.rank
  return <section aria-labelledby="recommendations-title"><div className="mb-3 flex items-end justify-between"><h2 id="recommendations-title" className="text-xl font-semibold">Recomendações</h2><p className="text-sm text-slate-600">{result.total} recomendação(ões)</p></div><div className="space-y-4">{result.recommendations.map((item) => { const best = item.rank === bestRank; return <Card key={`${item.rank}-${item.offer.provider}`} className={best ? 'border-sky-500 ring-2 ring-sky-100' : ''}><div className="flex flex-wrap items-center gap-2"><Badge>#{item.rank}</Badge>{best && <Badge className="bg-sky-100 text-sky-800">Melhor recomendação</Badge>}<strong>{item.offer.provider}</strong><span className="ml-auto font-bold">{item.offer.currency} {item.offer.price}</span></div><div className="mt-4 grid grid-cols-2 gap-3 text-sm sm:grid-cols-4"><p>Geral <strong>{item.score.overall_score}</strong></p><p>Preço <strong>{item.score.price_score}</strong></p><p>Duração <strong>{item.score.duration_score}</strong></p><p>Provider <strong>{item.score.provider_score}</strong></p></div>{item.reasons.length > 0 && <ul className="mt-4 list-disc space-y-1 pl-5 text-sm text-slate-600">{item.reasons.map((reason) => <li key={reason}>{reason}</li>)}</ul>}</Card> })}</div></section>
}

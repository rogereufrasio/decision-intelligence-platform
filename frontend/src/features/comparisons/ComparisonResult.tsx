import { Badge } from '../../components/ui/Badge'
import { Card } from '../../components/ui/Card'
import type { SearchComparisonResponse } from '../../types/comparison'
import { formatCurrency } from '../history/formatters'

export function ComparisonResult({ result }: { result: SearchComparisonResponse }) {
  const difference = Number(result.absolute_price_difference)
  const label = difference > 0 ? 'Aumento' : difference < 0 ? 'Redução' : 'Estável'
  const style = difference > 0 ? 'bg-rose-100 text-rose-800' : difference < 0 ? 'bg-emerald-100 text-emerald-800' : ''
  return <section aria-labelledby="comparison-result"><div className="mb-3 flex items-center gap-3"><h2 id="comparison-result" className="text-xl font-semibold">Resultado da comparação</h2><Badge className={style}>{label}</Badge></div><div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3"><Card><p className="text-sm text-slate-600">Melhor preço base</p><strong>{formatCurrency(result.base_lowest_price, result.currency)}</strong><p>{result.base_best_provider} · {result.base_offer_count} oferta(s)</p></Card><Card><p className="text-sm text-slate-600">Melhor preço alvo</p><strong>{formatCurrency(result.target_lowest_price, result.currency)}</strong><p>{result.target_best_provider} · {result.target_offer_count} oferta(s)</p></Card><Card><p className="text-sm text-slate-600">Variação</p><strong>{formatCurrency(result.absolute_price_difference, result.currency)}</strong><p>{result.percentage_price_difference === null ? 'Percentual indisponível' : `${Number(result.percentage_price_difference).toLocaleString('pt-BR')}%`}</p></Card></div><div className="mt-3 grid gap-3 sm:grid-cols-2"><Card><h3 className="font-semibold">Providers adicionados</h3><p>{result.added_providers.join(', ') || 'Nenhum'}</p></Card><Card><h3 className="font-semibold">Providers removidos</h3><p>{result.removed_providers.join(', ') || 'Nenhum'}</p></Card></div></section>
}

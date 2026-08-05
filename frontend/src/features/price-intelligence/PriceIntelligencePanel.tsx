import { Alert } from '../../components/ui/Alert'
import { Badge } from '../../components/ui/Badge'
import { Card } from '../../components/ui/Card'
import { Loading } from '../../components/ui/Loading'
import type { PriceIntelligenceResponse } from '../../types/history'
import { formatCurrency, translateTrend } from '../history/formatters'

export function PriceIntelligencePanel({ data, loading, error }: { data: PriceIntelligenceResponse | null; loading: boolean; error: string | null }) {
  if (loading) return <Loading label="Analisando histórico de preços" />
  if (error) return <Alert>{error}</Alert>
  if (!data) return null
  const metrics = [['Preço atual', data.current_price], ['Preço anterior', data.previous_price], ['Mínimo', data.historical_min], ['Máximo', data.historical_max], ['Média', data.historical_average], ['Variação absoluta', data.absolute_change]] as const
  return <section aria-labelledby="price-title"><div className="mb-3 flex items-center gap-3"><h3 id="price-title" className="font-semibold">Inteligência de preços</h3><Badge>{translateTrend(data.trend)}</Badge></div><div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">{metrics.map(([label, value]) => <Card key={label}><p className="text-sm text-slate-600">{label}</p><p className="mt-1 font-bold">{formatCurrency(value, data.currency)}</p></Card>)}<Card><p className="text-sm text-slate-600">Variação percentual</p><p className="mt-1 font-bold">{data.percentage_change === null ? 'Não disponível' : `${Number(data.percentage_change).toLocaleString('pt-BR')}%`}</p></Card><Card><p className="text-sm text-slate-600">Snapshots analisados</p><p className="mt-1 font-bold">{data.snapshot_count}</p></Card></div>{data.trend === 'insufficient_data' && <p className="mt-3 text-sm text-slate-600">Ainda não há dados suficientes para identificar uma tendência.</p>}</section>
}

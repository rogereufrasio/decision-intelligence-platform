import { Alert } from '../../components/ui/Alert'
import { Button } from '../../components/ui/Button'
import { Card } from '../../components/ui/Card'
import { EmptyState } from '../../components/ui/EmptyState'
import { Loading } from '../../components/ui/Loading'
import { formatDate } from '../history/formatters'
import { useDashboardData } from './useDashboardData'

export function OperationalDashboard() {
  const { metrics, recent, refresh } = useDashboardData()
  return <section aria-labelledby="operational-title" className="space-y-5"><div className="flex items-center justify-between"><h2 id="operational-title" className="text-lg font-semibold">Operação e atividade</h2><Button variant="secondary" onClick={refresh} disabled={metrics.loading || recent.loading}>Atualizar dashboard</Button></div>
    {metrics.loading ? <Loading label="Carregando métricas" /> : metrics.error ? <Alert>{metrics.error}</Alert> : metrics.data && <div className="grid gap-4 sm:grid-cols-3"><Card><p className="text-sm text-slate-600">Total de requests</p><p className="mt-2 text-2xl font-bold">{metrics.data.total_requests}</p></Card><Card><p className="text-sm text-slate-600">Total de erros</p><p className="mt-2 text-2xl font-bold">{metrics.data.total_errors}</p></Card><Card><p className="text-sm text-slate-600">Tempo médio</p><p className="mt-2 text-2xl font-bold">{metrics.data.average_response_time_ms.toLocaleString('pt-BR', { maximumFractionDigits: 2 })} ms</p></Card></div>}
    {recent.loading ? <Loading label="Carregando buscas recentes" /> : recent.error ? <Alert>{recent.error}</Alert> : recent.data?.items.length === 0 ? <EmptyState title="Nenhuma busca recente" description="As buscas persistidas aparecerão aqui." /> : recent.data && <div><h3 className="mb-3 font-semibold">Buscas recentes</h3><div className="grid gap-3 sm:grid-cols-2">{recent.data.items.map((item) => <Card key={item.search_id}><p className="font-semibold">{item.criteria.origin} → {item.criteria.destination}</p><p className="mt-1 text-sm text-slate-600">{formatDate(item.created_at, true)} · {item.offers.length} oferta(s)</p></Card>)}</div></div>}
  </section>
}

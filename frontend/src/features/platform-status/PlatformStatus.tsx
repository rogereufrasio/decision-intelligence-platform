import { Alert } from '../../components/ui/Alert'
import { Badge } from '../../components/ui/Badge'
import { Card } from '../../components/ui/Card'
import { Loading } from '../../components/ui/Loading'
import { usePlatformStatus } from './usePlatformStatus'

export function PlatformStatus() {
  const { loading, health, readiness, error } = usePlatformStatus()
  if (loading) return <Card><Loading label="Verificando a plataforma" /></Card>
  if (error) return <Alert><strong>Serviço indisponível.</strong> {error}</Alert>
  if (!health || !readiness) return <Alert>Nenhum status foi retornado pela API.</Alert>
  const ready = readiness.status === 'ready'
  return (
    <section aria-labelledby="platform-status-title">
      <h2 id="platform-status-title" className="mb-3 text-lg font-semibold">Status da plataforma</h2>
      <div className="grid gap-4 sm:grid-cols-2">
        <Card><div className="flex items-center justify-between"><h3 className="font-semibold">API</h3><Badge className="bg-emerald-100 text-emerald-800">Disponível</Badge></div><p className="mt-3 text-sm text-slate-600">{health.service} · versão {health.version}</p></Card>
        <Card><div className="flex items-center justify-between"><h3 className="font-semibold">Readiness</h3><Badge className={ready ? 'bg-emerald-100 text-emerald-800' : 'bg-amber-100 text-amber-800'}>{ready ? 'Pronta' : 'Atenção'}</Badge></div><p className="mt-3 text-sm text-slate-600">{readiness.checks.length} verificações operacionais.</p></Card>
      </div>
    </section>
  )
}

import { useState } from 'react'
import { Alert } from '../components/ui/Alert'
import { Badge } from '../components/ui/Badge'
import { Card } from '../components/ui/Card'
import { Loading } from '../components/ui/Loading'
import { PageHeader } from '../components/ui/PageHeader'
import { Select } from '../components/ui/Select'
import { API_BASE_URL } from '../lib/api/client'
import { getPreferredProvider, savePreferredProvider } from '../features/settings/providerPreference'
import { useSettingsStatus } from '../features/settings/useSettingsStatus'
import type { TravelProvider } from '../types/travel'

export function SettingsPage() {
  const [provider, setProvider] = useState(getPreferredProvider)
  const status = useSettingsStatus()
  function update(value: TravelProvider) { setProvider(value); savePreferredProvider(value) }
  return <><PageHeader title="Configurações" description="Preferências locais e conexão operacional da aplicação web." /><div className="grid gap-4 lg:grid-cols-2"><Card><h2 className="font-semibold">Conexão com a API</h2><p className="mt-2 break-all text-sm text-slate-600">{API_BASE_URL || 'Mesma origem da aplicação'}</p>{status.loading ? <Loading label="Consultando status" /> : status.error ? <Alert className="mt-3">{status.error}</Alert> : <div className="mt-3 flex flex-wrap gap-2"><Badge>API: {status.health?.status}</Badge><Badge>Readiness: {status.readiness?.status}</Badge></div>}</Card><Card><h2 className="font-semibold">Provider preferido: {provider}</h2><div className="mt-3"><Select label="Provider padrão das buscas" value={provider} onChange={(event) => update(event.target.value as TravelProvider)}><option value="mock">Mock</option><option value="amadeus">Amadeus</option><option value="duffel">Duffel</option></Select></div><p className="mt-3 text-sm text-slate-600">Esta preferência fica somente neste navegador. Credenciais do Amadeus e Duffel são configuradas exclusivamente no backend.</p></Card><Card><h2 className="font-semibold">Persistência</h2><p className="mt-2 text-sm text-slate-600">Histórico, decisões e exportações dependem da persistência configurada no backend. A API atual não publica um status específico; por isso esta tela não presume que ela esteja habilitada.</p></Card><Card><h2 className="font-semibold">IA assistiva</h2><p className="mt-2 text-sm text-slate-600">Habilitação e adapter pertencem ao backend. A API atual não publica esse estado nas configurações.</p></Card></div><Alert className="mt-4">A aplicação web nunca solicita nem armazena API keys ou secrets.</Alert></>
}

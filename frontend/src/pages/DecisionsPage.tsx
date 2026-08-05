import { Alert } from '../components/ui/Alert'
import { Button } from '../components/ui/Button'
import { EmptyState } from '../components/ui/EmptyState'
import { Loading } from '../components/ui/Loading'
import { PageHeader } from '../components/ui/PageHeader'
import { DecisionDetail } from '../features/decisions/DecisionDetail'
import { DecisionList } from '../features/decisions/DecisionList'
import { useDecisionHistory } from '../features/decisions/useDecisionHistory'
import { ExportButton } from '../features/search-export/ExportButton'

export function DecisionsPage() {
  const state = useDecisionHistory()
  return <><PageHeader title="Decisões" description="Acompanhe decisões persistidas e suas explicações determinísticas." /><div className="mb-5"><Button variant="secondary" onClick={state.refresh} disabled={state.loading}>Atualizar decisões</Button></div>{state.loading ? <Loading label="Carregando decisões" /> : state.error ? <Alert>{state.error}</Alert> : state.data?.items.length === 0 ? <EmptyState title="Nenhuma decisão carregada" description="O histórico de decisões está vazio." /> : state.data && <DecisionList items={state.data.items} onSelect={state.select} />}<div className="mt-6"><DecisionDetail item={state.selected} />{state.selected?.search_id && <div className="mt-3"><ExportButton searchId={state.selected.search_id} /></div>}</div></>
}

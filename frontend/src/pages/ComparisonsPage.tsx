import { Alert } from '../components/ui/Alert'
import { Button } from '../components/ui/Button'
import { Card } from '../components/ui/Card'
import { EmptyState } from '../components/ui/EmptyState'
import { Loading } from '../components/ui/Loading'
import { PageHeader } from '../components/ui/PageHeader'
import { ComparisonResult } from '../features/comparisons/ComparisonResult'
import { useComparison } from '../features/comparisons/useComparison'
import { formatDate } from '../features/history/formatters'
import { ExportButton } from '../features/search-export/ExportButton'

export function ComparisonsPage() {
  const state = useComparison()
  return <><PageHeader title="Comparações" description="Compare preços, providers e ofertas entre duas buscas persistidas." /><div className="mb-5 flex flex-wrap gap-3"><Button variant="secondary" onClick={state.refresh} disabled={state.loadingList}>Atualizar</Button><Button variant="secondary" onClick={state.clear} disabled={state.selected.length === 0}>Limpar seleção</Button><Button onClick={state.compare} loading={state.loading} disabled={state.selected.length !== 2}>Comparar selecionadas</Button></div>{state.loadingList ? <Loading label="Carregando buscas" /> : state.listError ? <Alert>{state.listError}</Alert> : state.snapshots.length === 0 ? <EmptyState title="Nenhuma busca disponível" description="O histórico ainda não possui snapshots para comparar." /> : <section aria-label="Snapshots para comparação" className="grid gap-3 md:grid-cols-2">{state.snapshots.map((snapshot) => { const checked = state.selected.includes(snapshot.search_id); return <Card key={snapshot.search_id} className={checked ? 'border-sky-500 ring-2 ring-sky-200' : ''}><label className="flex cursor-pointer items-start gap-3"><input type="checkbox" checked={checked} onChange={() => state.toggle(snapshot.search_id)} /><span><strong>{snapshot.criteria.origin} → {snapshot.criteria.destination}</strong><span className="block text-sm text-slate-600">{formatDate(snapshot.created_at, true)} · {snapshot.provider}</span></span></label>{checked && <div className="mt-3"><ExportButton searchId={snapshot.search_id} /></div>}</Card>})}</section>}{state.selected.length > 0 && <p role="status" className="my-4 text-sm">{state.selected.length} de 2 snapshots selecionados.</p>}{state.error && <Alert>{state.error}</Alert>}{state.result && <ComparisonResult result={state.result} />}</>
}

import { useState } from 'react'
import { Alert } from '../components/ui/Alert'
import { Button } from '../components/ui/Button'
import { EmptyState } from '../components/ui/EmptyState'
import { Loading } from '../components/ui/Loading'
import { PageHeader } from '../components/ui/PageHeader'
import { HistoryList, type HistoryFilters } from '../features/history/HistoryList'
import { SnapshotDetail } from '../features/history/SnapshotDetail'
import { useSearchHistory } from '../features/history/useSearchHistory'
import { PriceIntelligencePanel } from '../features/price-intelligence/PriceIntelligencePanel'
import { usePriceIntelligence } from '../features/price-intelligence/usePriceIntelligence'

const initialFilters: HistoryFilters = { origin: '', destination: '', provider: '', status: '' }

export function HistoryPage() {
  const history = useSearchHistory()
  const price = usePriceIntelligence()
  const [filters, setFilters] = useState(initialFilters)
  function select(searchId: string) { void history.select(searchId); void price.load(searchId) }
  return <><PageHeader title="Histórico" description="Consulte buscas persistidas, ofertas e inteligência histórica de preços." /><div className="mb-5"><Button variant="secondary" onClick={history.refresh} disabled={history.loading}>Atualizar histórico</Button></div><div className="space-y-7" aria-live="polite">{history.loading ? <Loading label="Carregando histórico" /> : history.error ? <Alert>{history.error}</Alert> : history.history?.items.length === 0 ? <EmptyState title="Histórico vazio" description="Nenhuma busca carregada" /> : history.history && <HistoryList items={history.history.items} filters={filters} onFiltersChange={setFilters} onSelect={select} onLoadMore={history.loadMore} canLoadMore={history.limit < 100 && history.history.total >= history.limit} />}<SnapshotDetail snapshot={history.detail} loading={history.detailLoading} error={history.detailError} /><PriceIntelligencePanel data={price.data} loading={price.loading} error={price.error} /></div></>
}

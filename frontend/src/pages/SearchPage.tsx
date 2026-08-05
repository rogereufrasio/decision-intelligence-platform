import { Alert } from '../components/ui/Alert'
import { Loading } from '../components/ui/Loading'
import { PageHeader } from '../components/ui/PageHeader'
import { RecommendationResults } from '../features/recommendations/RecommendationResults'
import { SearchForm } from '../features/search/SearchForm'
import { SearchResults } from '../features/search/SearchResults'
import { useTravelSearch } from '../features/search/useTravelSearch'

export function SearchPage() {
  const state = useTravelSearch()
  return <><PageHeader title="Buscar viagem" description="Encontre ofertas e receba recomendações conforme suas preferências." /><SearchForm onSubmit={state.submit} loading={state.searchLoading || state.recommendationLoading} /><div className="mt-6 space-y-6" aria-live="polite">{state.searchLoading && <Loading label="Buscando ofertas" />}{state.searchError && <Alert>{state.searchError}</Alert>}{state.searchResult && <SearchResults result={state.searchResult} />}{state.recommendationLoading && <Loading label="Analisando recomendações" />}{state.recommendationError && <Alert>{state.recommendationError}</Alert>}{state.recommendations && <RecommendationResults result={state.recommendations} />}{state.correlationId && <p className="text-xs text-slate-500">Referência: {state.correlationId}</p>}</div></>
}

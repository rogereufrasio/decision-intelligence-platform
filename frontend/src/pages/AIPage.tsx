import { Alert } from '../components/ui/Alert'
import { Card } from '../components/ui/Card'
import { PageHeader } from '../components/ui/PageHeader'

export function AIPage() {
  return <><PageHeader title="IA assistiva" description="Entenda o papel da explicação assistida na plataforma." /><Card><h2 className="text-lg font-semibold">Capacidade opcional do backend</h2><p className="mt-2 text-sm text-slate-600">A IA assistiva explica contextos completos de decisão por meio de um contrato independente de fornecedor. Esta interface ainda não possui um fluxo de criação de contexto suficientemente definido para enviar explicações com segurança.</p></Card><Alert className="mt-4">Nenhuma explicação é fabricada e nenhuma chamada é feita sem um contexto de decisão válido. A habilitação e o adapter são configurados exclusivamente no backend.</Alert></>
}

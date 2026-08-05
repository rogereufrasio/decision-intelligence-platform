import { Card } from '../components/ui/Card'; import { PageHeader } from '../components/ui/PageHeader'
export function SettingsPage() { return <><PageHeader title="Configurações" description="Informações locais da aplicação web." /><Card><p className="text-sm text-slate-600">A URL da API é definida por ambiente. Nenhuma credencial é armazenada nesta aplicação.</p></Card></> }

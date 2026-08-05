import { Link } from 'react-router-dom'
import { PageHeader } from '../components/ui/PageHeader'
export function NotFoundPage() { return <><PageHeader title="Página não encontrada" description="O endereço informado não existe nesta aplicação." /><Link className="font-semibold text-sky-700 hover:text-sky-900" to="/">Voltar ao Dashboard</Link></> }

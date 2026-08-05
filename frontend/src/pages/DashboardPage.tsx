import { PageHeader } from '../components/ui/PageHeader'
import { PlatformStatus } from '../features/platform-status/PlatformStatus'
import { OperationalDashboard } from '../features/dashboard/OperationalDashboard'
export function DashboardPage() { return <><PageHeader title="Dashboard" description="Visão geral da disponibilidade e operação da Decision Intelligence Platform." /><div className="space-y-8"><PlatformStatus /><OperationalDashboard /></div></> }

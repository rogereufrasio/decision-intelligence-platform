import { Route, Routes } from 'react-router-dom'
import { AppLayout } from '../components/layout/AppLayout'
import { AIPage } from '../pages/AIPage'
import { ComparisonsPage } from '../pages/ComparisonsPage'
import { DashboardPage } from '../pages/DashboardPage'
import { DecisionsPage } from '../pages/DecisionsPage'
import { HistoryPage } from '../pages/HistoryPage'
import { NotFoundPage } from '../pages/NotFoundPage'
import { SearchPage } from '../pages/SearchPage'
import { SettingsPage } from '../pages/SettingsPage'

export function AppRoutes() {
  return (
    <Routes>
      <Route element={<AppLayout />}>
        <Route index element={<DashboardPage />} />
        <Route path="buscar" element={<SearchPage />} />
        <Route path="historico" element={<HistoryPage />} />
        <Route path="comparacoes" element={<ComparisonsPage />} />
        <Route path="decisoes" element={<DecisionsPage />} />
        <Route path="ia-assistiva" element={<AIPage />} />
        <Route path="configuracoes" element={<SettingsPage />} />
        <Route path="*" element={<NotFoundPage />} />
      </Route>
    </Routes>
  )
}

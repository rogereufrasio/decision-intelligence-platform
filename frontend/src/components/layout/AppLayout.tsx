import { useState } from 'react'
import { NavLink, Outlet } from 'react-router-dom'
import { Button } from '../ui/Button'

const navigation = [
  ['/', 'Dashboard'], ['/buscar', 'Buscar viagem'], ['/historico', 'Histórico'],
  ['/comparacoes', 'Comparações'], ['/decisoes', 'Decisões'], ['/ia-assistiva', 'IA assistiva'], ['/configuracoes', 'Configurações'],
] as const

function Navigation({ onNavigate }: { onNavigate?: () => void }) {
  return (
    <nav aria-label="Navegação principal" className="space-y-1">
      {navigation.map(([to, label]) => (
        <NavLink key={to} to={to} end={to === '/'} onClick={onNavigate}
          className={({ isActive }) => `block rounded-lg px-3 py-2 text-sm font-medium transition ${isActive ? 'bg-sky-100 text-ocean' : 'text-slate-600 hover:bg-slate-100 hover:text-ink'}`}>
          {label}
        </NavLink>
      ))}
    </nav>
  )
}

export function AppLayout() {
  const [mobileOpen, setMobileOpen] = useState(false)
  return (
    <div className="min-h-screen">
      <header className="sticky top-0 z-30 border-b border-slate-200 bg-white">
        <div className="flex h-16 items-center justify-between px-4 lg:px-6">
          <div><p className="text-xs font-semibold uppercase tracking-widest text-sky-700">DIP</p><p className="font-semibold">Decision Intelligence</p></div>
          <Button className="lg:hidden" variant="secondary" aria-expanded={mobileOpen} aria-controls="mobile-navigation" onClick={() => setMobileOpen((value) => !value)}>
            {mobileOpen ? 'Fechar menu' : 'Abrir menu'}
          </Button>
        </div>
      </header>
      <div className="mx-auto flex max-w-screen-2xl">
        <aside className="hidden min-h-[calc(100vh-4rem)] w-64 border-r border-slate-200 bg-white p-4 lg:block"><Navigation /></aside>
        {mobileOpen && <div id="mobile-navigation" className="fixed inset-x-0 top-16 z-20 border-b border-slate-200 bg-white p-4 shadow-lg lg:hidden"><Navigation onNavigate={() => setMobileOpen(false)} /></div>}
        <main id="conteudo-principal" className="min-w-0 flex-1 p-4 sm:p-6 lg:p-8"><Outlet /></main>
      </div>
    </div>
  )
}

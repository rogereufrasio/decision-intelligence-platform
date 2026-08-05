export function formatDate(value: string | null, includeTime = false) {
  if (!value) return 'Não informada'
  const date = includeTime ? new Date(value) : new Date(`${value}T00:00:00`)
  return new Intl.DateTimeFormat('pt-BR', includeTime ? { dateStyle: 'short', timeStyle: 'short' } : { dateStyle: 'short' }).format(date)
}

export function formatCurrency(value: string | null, currency: string | null) {
  if (value === null || currency === null) return 'Não disponível'
  return new Intl.NumberFormat('pt-BR', { style: 'currency', currency }).format(Number(value))
}

export function translateTrend(trend: string) {
  return ({ decreased: 'Em queda', increased: 'Em alta', stable: 'Estável', insufficient_data: 'Dados insuficientes' } as Record<string, string>)[trend] ?? trend
}

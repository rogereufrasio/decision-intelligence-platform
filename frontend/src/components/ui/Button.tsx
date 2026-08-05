import type { ButtonHTMLAttributes } from 'react'

type Props = ButtonHTMLAttributes<HTMLButtonElement> & { variant?: 'primary' | 'secondary'; loading?: boolean }
export function Button({ variant = 'primary', loading = false, disabled, className = '', children, ...props }: Props) {
  const styles = variant === 'primary' ? 'bg-sky-700 text-white hover:bg-sky-800' : 'border border-slate-300 bg-white text-ink hover:bg-slate-50'
  return <button className={`inline-flex min-h-10 items-center justify-center rounded-lg px-4 py-2 text-sm font-semibold transition disabled:cursor-not-allowed disabled:opacity-50 ${styles} ${className}`} disabled={disabled || loading} {...props}>{loading ? 'Carregando…' : children}</button>
}

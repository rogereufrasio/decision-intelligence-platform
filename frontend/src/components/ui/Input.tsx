import type { InputHTMLAttributes } from 'react'
type Props = InputHTMLAttributes<HTMLInputElement> & { label: string }
export function Input({ label, id, className = '', ...props }: Props) {
  const inputId = id ?? props.name
  return <label className="block text-sm font-medium text-slate-700" htmlFor={inputId}>{label}<input id={inputId} className={`mt-1 block w-full rounded-lg border border-slate-300 bg-white px-3 py-2 disabled:bg-slate-100 ${className}`} {...props} /></label>
}

import type { SelectHTMLAttributes } from 'react'
type Props = SelectHTMLAttributes<HTMLSelectElement> & { label: string }
export function Select({ label, id, className = '', children, ...props }: Props) {
  const selectId = id ?? props.name
  return <label className="block text-sm font-medium text-slate-700" htmlFor={selectId}>{label}<select id={selectId} className={`mt-1 block w-full rounded-lg border border-slate-300 bg-white px-3 py-2 disabled:bg-slate-100 ${className}`} {...props}>{children}</select></label>
}

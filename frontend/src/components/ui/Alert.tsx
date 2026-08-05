import type { HTMLAttributes } from 'react'
export function Alert({ className = '', ...props }: HTMLAttributes<HTMLDivElement>) { return <div role="alert" className={`rounded-lg border border-amber-300 bg-amber-50 p-4 text-sm text-amber-900 ${className}`} {...props} /> }

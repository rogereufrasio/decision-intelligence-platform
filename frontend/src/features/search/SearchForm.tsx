import { useState, type FormEvent } from 'react'
import { Button } from '../../components/ui/Button'
import { Input } from '../../components/ui/Input'
import { Select } from '../../components/ui/Select'
import type { SearchFormValues } from '../../types/travel'

const initialValues: SearchFormValues = { origin: '', destination: '', departureDate: '', returnDate: '', adults: 1, profile: 'balanced', preferredProviders: '' }

function validate(values: SearchFormValues) {
  const errors: Partial<Record<keyof SearchFormValues, string>> = {}
  if (!/^[A-Za-z]{3}$/.test(values.origin.trim())) errors.origin = 'Informe um código IATA de 3 letras.'
  if (!/^[A-Za-z]{3}$/.test(values.destination.trim())) errors.destination = 'Informe um código IATA de 3 letras.'
  if (!values.departureDate) errors.departureDate = 'Informe a data de ida.'
  if (values.returnDate && values.departureDate && values.returnDate < values.departureDate) errors.returnDate = 'A volta deve ser posterior à ida.'
  if (values.adults < 1) errors.adults = 'Informe ao menos um adulto.'
  return errors
}

export function SearchForm({ onSubmit, loading }: { onSubmit: (values: SearchFormValues) => Promise<void>; loading: boolean }) {
  const [values, setValues] = useState(initialValues)
  const [errors, setErrors] = useState<Partial<Record<keyof SearchFormValues, string>>>({})
  function update<K extends keyof SearchFormValues>(field: K, value: SearchFormValues[K]) { setValues((current) => ({ ...current, [field]: value })) }
  async function submit(event: FormEvent) {
    event.preventDefault(); const nextErrors = validate(values); setErrors(nextErrors)
    if (Object.keys(nextErrors).length) return
    await onSubmit(values)
  }
  const error = (field: keyof SearchFormValues) => errors[field] ? <p id={`${field}-error`} className="mt-1 text-sm text-red-700">{errors[field]}</p> : null
  return (
    <form onSubmit={submit} noValidate className="rounded-xl border border-slate-200 bg-white p-5 shadow-sm" aria-label="Busca de viagens">
      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        <div><Input label="Origem" name="origin" value={values.origin} maxLength={3} aria-invalid={Boolean(errors.origin)} aria-describedby={errors.origin ? 'origin-error' : undefined} onChange={(event) => update('origin', event.target.value)} />{error('origin')}</div>
        <div><Input label="Destino" name="destination" value={values.destination} maxLength={3} aria-invalid={Boolean(errors.destination)} aria-describedby={errors.destination ? 'destination-error' : undefined} onChange={(event) => update('destination', event.target.value)} />{error('destination')}</div>
        <div><Input label="Data de ida" name="departureDate" type="date" value={values.departureDate} aria-invalid={Boolean(errors.departureDate)} aria-describedby={errors.departureDate ? 'departureDate-error' : undefined} onChange={(event) => update('departureDate', event.target.value)} />{error('departureDate')}</div>
        <div><Input label="Data de volta (opcional)" name="returnDate" type="date" value={values.returnDate} aria-invalid={Boolean(errors.returnDate)} aria-describedby={errors.returnDate ? 'returnDate-error' : undefined} onChange={(event) => update('returnDate', event.target.value)} />{error('returnDate')}</div>
        <div><Input label="Adultos" name="adults" type="number" min={1} value={values.adults} aria-invalid={Boolean(errors.adults)} aria-describedby={errors.adults ? 'adults-error' : undefined} onChange={(event) => update('adults', Number(event.target.value))} />{error('adults')}</div>
        <Select label="Perfil de preferência" name="profile" value={values.profile} onChange={(event) => update('profile', event.target.value as SearchFormValues['profile'])}><option value="cheapest">Menor preço</option><option value="fastest">Mais rápido</option><option value="balanced">Equilibrado</option><option value="premium">Premium</option></Select>
      </div>
      <div className="mt-4"><Input label="Providers preferidos (opcional, separados por vírgula)" name="preferredProviders" value={values.preferredProviders} onChange={(event) => update('preferredProviders', event.target.value)} /></div>
      <div className="mt-5"><Button type="submit" loading={loading}>{loading ? 'Buscando…' : 'Buscar viagens'}</Button></div>
    </form>
  )
}

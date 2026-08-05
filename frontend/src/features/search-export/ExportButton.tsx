import { useState } from 'react'
import { Alert } from '../../components/ui/Alert'
import { Button } from '../../components/ui/Button'
import { exportSearchSnapshot } from './api'

function fileName(path: string) { return path.split(/[\\/]/).pop() ?? path }

export function ExportButton({ searchId }: { searchId: string }) {
  const [loading, setLoading] = useState(false)
  const [message, setMessage] = useState<string | null>(null)
  const [error, setError] = useState<string | null>(null)
  async function run() {
    setLoading(true); setMessage(null); setError(null)
    try {
      const result = await exportSearchSnapshot(searchId)
      const link = document.createElement('a'); link.href = result.file; link.download = fileName(result.file); link.click()
      setMessage(`Exportação preparada: ${link.download}`)
    } catch { setError('Não foi possível exportar o snapshot.') }
    finally { setLoading(false) }
  }
  return <div><Button variant="secondary" loading={loading} onClick={run}>Exportar Parquet</Button>{message && <p role="status" className="mt-2 text-sm text-emerald-700">{message}</p>}{error && <Alert className="mt-2">{error}</Alert>}</div>
}

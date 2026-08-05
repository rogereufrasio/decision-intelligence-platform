export interface ApiErrorPayload {
  detail?: string | { code?: string; message?: string }
}

export class ApiError extends Error {
  constructor(
    message: string,
    public readonly status: number,
    public readonly code: string,
    public readonly correlationId: string | null,
  ) {
    super(message)
    this.name = 'ApiError'
  }
}

export interface HealthResponse {
  status: string
  service: string
  version: string
}

export interface ReadinessCheck {
  name: string
  status: string
  message: string
}

export interface ReadinessResponse {
  status: string
  checks: ReadinessCheck[]
}

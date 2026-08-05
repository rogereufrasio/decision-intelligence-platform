# Decision Intelligence Platform

> Make better decisions through data, analytics and AI.

The MVP is a modular-monolith reference implementation for travel decision
intelligence. It searches canonical offers, ranks and recommends them, applies
deterministic rules, explains decisions, analyzes price history, and optionally
adds a local assistive explanation without making AI a domain dependency.

## Architecture

```text
FastAPI API
  -> application use cases and ports
  -> domain models and deterministic engines
  -> infrastructure adapters (providers, DuckDB, Parquet, template AI)
```

The backend follows Clean Architecture, DDD, provider/strategy patterns and
strong typing. Search and decision persistence are optional and local.

## Backend quick start

Python 3.14 and [uv](https://docs.astral.sh/uv/) are required.

```powershell
cd backend
uv sync --frozen
uv run uvicorn src.main:app --reload
```

The API is available at `http://127.0.0.1:8000`; interactive OpenAPI docs are
at `/docs`.

```powershell
uv run pytest
uv run ruff check src tests
```

See [backend/README.md](backend/README.md) for configuration, endpoints,
persistence and operational details.

## Frontend v1.1

O shell web em React/Vite está disponível em `frontend/`, com navegação
responsiva, design system mínimo e monitoramento inicial de health/readiness.

```powershell
cd frontend
npm install
npm run dev
```

O Vite encaminha `/api` para `http://localhost:8000` no desenvolvimento local.
Configure `VITE_API_BASE_URL` apenas para outra origem. Consulte [frontend/README.md](frontend/README.md) para
estrutura, testes e build.

## MVP scope

- Multi-provider travel search and canonical offers
- Deterministic ranking, recommendations, rules and explanations
- Search/decision history, price intelligence and Parquet export
- Optional template-based assistive AI behind an application port
- Correlation IDs, structured request logs, in-memory metrics, security headers,
  health and readiness
- Locked dependencies and GitHub Actions backend CI

## Known limitations

This MVP uses local DuckDB files and process-local metrics, has no authentication
or distributed tracing, and performs no real LLM integration. Provider
credentials and production deployment controls remain environment-specific.

Operational acceptance is documented in
[DIP-013 MVP Operational Readiness](docs/product/DIP-013-mvp-operational-readiness.md).

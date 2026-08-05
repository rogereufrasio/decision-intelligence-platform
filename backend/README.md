# Decision Intelligence Platform Backend

FastAPI backend for the travel-focused Decision Intelligence Platform MVP.
It separates domain engines, application ports/use cases and infrastructure
adapters in a modular monolith.

## Setup and local execution

Requirements: Python 3.14 and `uv`.

```powershell
cd backend
uv sync --frozen
uv run uvicorn src.main:app --reload
```

Quality checks:

```powershell
uv run python -m compileall -q src tests
uv run ruff check src tests
uv run pytest
```

## Configuration

Safe defaults keep external providers, persistence and assistive AI disabled.
Environment variables are case-insensitive. Example only—do not commit secrets:

```dotenv
APP_ENVIRONMENT=development
TRAVEL_PROVIDER=mock
SEARCH_PERSISTENCE_ENABLED=false
SEARCH_DATABASE_PATH=../data/searches.duckdb
DECISION_PERSISTENCE_ENABLED=false
DECISION_DATABASE_PATH=../data/decisions.duckdb
AI_ASSISTANT_ENABLED=false
AI_ASSISTANT_PROVIDER=template
OBSERVABILITY_ENABLED=true
METRICS_ENABLED=true
SECURITY_HEADERS_ENABLED=true
READINESS_ENABLED=true
EXTERNAL_DEPENDENCY_CHECK_ENABLED=false
HTTP_TIMEOUT_SECONDS=30
AMADEUS_CLIENT_ID=
AMADEUS_CLIENT_SECRET=
DUFFEL_API_KEY=
```

Provider credentials are required only when their provider is selected and
external configuration checks are enabled. Never place real values in tracked
files.

## Persistence and assistive AI

When enabled, searches and decisions are stored in separate local DuckDB files.
Search snapshots can be exported to Parquet. Both formats are ignored by Git.
No migrations framework, remote database, or automatic decision persistence is
introduced in the MVP.

Assistive AI is optional and accessed through `AIAssistant`. The included
`template` adapter is deterministic and local: it performs no HTTP or LLM call.

## Main endpoints

| Method | Path | Purpose |
|---|---|---|
| GET | `/api/v1/health` | Liveness |
| GET | `/api/v1/readiness` | Operational readiness |
| GET | `/api/v1/metrics` | In-memory metrics |
| POST | `/api/v1/travel/search` | Generic travel search |
| POST | `/api/v1/flights/search` | Flight search |
| POST | `/api/v1/recommendations` | Ranked recommendations |
| GET | `/api/v1/search-history` | Search history |
| GET | `/api/v1/search-comparison` | Snapshot comparison |
| GET | `/api/v1/search-history/{search_id}/export` | Parquet export |
| GET | `/api/v1/price-intelligence/{search_id}` | Price intelligence |
| GET | `/api/v1/decision-history` | Decision history |
| POST | `/api/v1/ai-explanations` | Optional assisted explanation |

## Travel provider selection and Parquet download

`POST /api/v1/flights/search` accepts the optional `X-Travel-Provider` header
with `mock`, `amadeus`, or `duffel`. Without it, `TRAVEL_PROVIDER` is used and
defaults to `mock`. Amadeus and Duffel credentials remain server-side environment
variables and are never returned in responses or readiness messages.

`GET /api/v1/search-history/{search_id}/export` returns the Parquet bytes with a
safe attachment filename. It does not expose the server filesystem path.

## Operational behavior and limitations

Every response receives a correlation ID and security headers. Request logs are
structured; metrics are thread-safe but process-local. Readiness validates local
configuration and directories without calling providers or creating databases.

The MVP does not include authentication, rate limiting, distributed metrics,
distributed tracing, managed persistence, production secret management, or a
real generative-AI adapter. Third-party TestClient deprecation warnings are
accepted until a safe upstream migration is planned.

## Integration with the v1.1 web product

The React frontend runs on port `5173` and the API on `8000`. Configure allowed
origins with `CORS_ALLOWED_ORIGINS`; wildcard origins and browser credentials are
not enabled. Search provider selection uses `X-Travel-Provider`, while Amadeus
and Duffel secrets remain server-side. The local template AI adapter is optional
and does not perform an LLM or external HTTP call.

Run backend validation with `uv run pytest` and `uv run ruff check src tests`.
The root scripts start the integrated product and execute isolated Chromium E2E.

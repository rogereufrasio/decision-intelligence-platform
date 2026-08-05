# DIP-014 — Product MVP v1.1

## Status

Accepted for release on 2026-08-05.

## Objective

Version 1.1 turns the backend MVP into an operable web product while preserving
the modular-monolith architecture and deterministic decision-intelligence core.

## Delivered scope

- Responsive React, Vite and TypeScript frontend with accessible navigation.
- Dashboard for health, readiness, metrics and recent searches.
- Travel search with mock, Amadeus or Duffel selection and canonical results.
- Recommendation presentation with profile, rank, scores and reasons.
- Persisted search history, snapshot details and price-intelligence indicators.
- Two-snapshot comparison with price and provider changes.
- Decision history with accepted/rejected recommendations and explanations.
- Binary Parquet download from history and comparisons.
- Local settings for API URL and provider preference; no browser credentials.
- Informative AI-assistance page reflecting the optional backend capability.

## Architecture and operations

The frontend calls the FastAPI modular monolith through a typed Fetch client.
`X-Correlation-ID` is propagated and `X-Travel-Provider` carries only the local
provider preference. DuckDB and Parquet remain optional local adapters. AI remains
behind an application port with a deterministic template adapter.

The backend exposes health, readiness, security headers, structured logs and
in-memory metrics. CORS is restricted to configured origins. Amadeus and Duffel
secrets exist only in backend environment variables.

## Quality and tests

- Backend unit and integration tests plus Ruff.
- Frontend component/integration tests, ESLint and production build.
- Chromium E2E covering dashboard, settings, search, recommendation, history,
  price intelligence, comparison, export, decision state, AI state and 404.
- CI runs backend, frontend and E2E jobs; browser artifacts are retained only on
  failure.

## Residual risks

- DuckDB is local and unsuitable for horizontal multi-instance writes.
- Metrics are process-local; authentication and rate limiting are not included.
- Real-provider operation depends on external credentials, quotas and availability.
- AI assistance has no end-user context-composition workflow in v1.1.
- The npm dependency audit reports known high-severity advisories requiring a
  separately assessed upgrade rather than a forced breaking update.

## Acceptance criteria

- All supported pages render on desktop and mobile with keyboard navigation.
- Mock search produces an offer and recommendation without external services.
- Persisted searches can be inspected, compared and exported as valid Parquet.
- Backend, frontend and E2E suites pass without runtime artifacts or secrets.
- Setup, configuration, limitations and operational scripts are documented.

## Outside v1.1

Authentication, managed databases, distributed observability, production secret
management, richer analytics charts, automated decision creation and generative
AI adapters remain future work.

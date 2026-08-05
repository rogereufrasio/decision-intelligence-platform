# DIP-013 — MVP Operational Readiness

**Status:** Ready for MVP closure  
**Version:** 1.0  
**Date:** 2026-08-05

## Scope delivered

The travel MVP delivers multi-provider search, canonical offers, deterministic
ranking and recommendations, decision rules and explanations, search and
decision history, price intelligence, Parquet export, and optional local
AI-assisted explanations. The solution remains a modular monolith.

## Components

- FastAPI API with versioned routes and OpenAPI
- Application use cases behind explicit ports
- Domain recommendation, price, rule and explanation engines
- Provider strategy/factory and canonical offer model
- DuckDB repositories and Parquet export
- Optional deterministic template AI adapter
- Operational middleware and readiness service

## Operational requirements

Python 3.14 and `uv` are required. Dependencies are resolved from
`backend/uv.lock`; CI installs them with `uv sync --frozen`. Safe defaults use the
mock travel provider and disable persistence, external dependency checks and AI.
Runtime secrets must be supplied through the deployment environment.

## Observability

Requests carry `X-Correlation-ID`, structured completion logs, elapsed time and
status. Thread-safe, process-local metrics report request totals, status groups,
errors and average response time through `/api/v1/metrics`.

## Security

API responses use `nosniff`, frame denial, no-referrer and no-store headers.
Bodies and secrets are excluded from request logs. The MVP does not yet provide
authentication, authorization, rate limiting or a production secrets manager.

## Health and readiness

`/api/v1/health` is dependency-free liveness. `/api/v1/readiness` validates
loaded configuration, HTTP client availability, enabled persistence directories
and minimum external-provider configuration. It does not call providers or
create database files.

## Persistence

Search and decision snapshots use separate optional DuckDB databases. Search
snapshots can be exported to Parquet. Database, Parquet, environment, log and
cache artifacts are excluded from version control.

## Continuous integration

GitHub Actions runs on pushes and pull requests using Ubuntu, Python 3.14 and
cached `uv` dependencies. It validates the frozen lock, compiles all Python
files, runs conservative Ruff checks and the complete pytest suite, and rejects
whitespace errors.

## Residual risks

- Local files are not suitable for horizontally scaled concurrent deployments.
- Metrics reset per process and are not exported to a monitoring platform.
- Provider availability is not actively probed by readiness.
- Authentication, rate limiting and distributed tracing remain future work.
- The template AI adapter is deterministic and not generative.
- A third-party Starlette TestClient deprecation warning remains non-blocking.

## MVP acceptance criteria

- All documented API routes appear in generated OpenAPI.
- Full backend tests, Python compilation, Ruff and whitespace checks pass.
- Defaults start without external credentials, databases or AI resources.
- Health, readiness, metrics, correlation IDs and security headers are active.
- No secrets or runtime data artifacts are versioned.
- Architecture remains clean, typed, testable and provider-independent.

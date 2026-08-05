# Changelog

All notable changes to the Decision Intelligence Platform are documented here.

## [1.1.0] - 2026-08-05

### Added

- React/Vite web application with responsive navigation and reusable UI components.
- Operational dashboard, travel search, deterministic recommendations, history,
  price intelligence, comparisons, decision history and Parquet downloads.
- Local provider preference for mock, Amadeus and Duffel without browser secrets.
- Informative AI-assistance page aligned with the existing optional backend port.
- Configurable CORS, integrated PowerShell development scripts and Playwright E2E.
- Frontend and browser validation in GitHub Actions.

### Changed

- Mock travel provider now returns a deterministic canonical offer for local use.
- Parquet export is delivered as an HTTP attachment without exposing server paths.

### Security

- Provider credentials remain backend-only.
- Runtime databases, Parquet files, environment files and Playwright artifacts are
  excluded from version control.

## [1.0.0]

- Backend MVP with search, decision intelligence, persistence, observability,
  readiness, security headers and optional template-based AI assistance.

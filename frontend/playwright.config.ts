import { defineConfig, devices } from '@playwright/test'

const baseURL = process.env.E2E_BASE_URL ?? 'http://127.0.0.1:5173'
const backendCommand = process.env.E2E_BACKEND_COMMAND ?? 'powershell -NoProfile -Command "$env:TRAVEL_PROVIDER=\'mock\'; $env:SEARCH_PERSISTENCE_ENABLED=\'true\'; $env:SEARCH_DATABASE_PATH=\'../.tmp/e2e-searches.duckdb\'; $env:DECISION_PERSISTENCE_ENABLED=\'true\'; $env:DECISION_DATABASE_PATH=\'../.tmp/e2e-decisions.duckdb\'; $env:AI_ASSISTANT_ENABLED=\'true\'; Set-Location ../backend; uv run uvicorn src.main:app --host 127.0.0.1 --port 8000"'

export default defineConfig({
  testDir: './e2e',
  fullyParallel: false,
  workers: 1,
  retries: 0,
  reporter: 'list',
  use: {
    baseURL,
    trace: 'retain-on-failure',
    screenshot: 'only-on-failure',
  },
  webServer: [
    { command: backendCommand, url: 'http://127.0.0.1:8000/api/v1/health', reuseExistingServer: false, timeout: 120_000 },
    { command: 'npm run dev -- --host 127.0.0.1', url: baseURL, reuseExistingServer: false, timeout: 120_000 },
  ],
  projects: [{ name: 'chromium', use: { ...devices['Desktop Chrome'] } }],
})

import { defineConfig, devices } from '@playwright/test'

const baseURL = process.env.E2E_BASE_URL ?? 'http://127.0.0.1:5173'
const backendCommand = process.env.E2E_BACKEND_COMMAND ?? 'uv run --project ../backend uvicorn src.main:app --app-dir ../backend --host 127.0.0.1 --port 8000'

export default defineConfig({
  testDir: './e2e',
  fullyParallel: false,
  workers: 1,
  retries: 0,
  reporter: 'list',
  globalSetup: './e2e/global-setup.ts',
  globalTeardown: './e2e/global-teardown.ts',
  use: {
    baseURL,
    trace: 'retain-on-failure',
    screenshot: 'only-on-failure',
  },
  webServer: [
    {
      command: backendCommand,
      url: 'http://127.0.0.1:8000/api/v1/health',
      reuseExistingServer: false,
      timeout: 120_000,
      env: {
        TRAVEL_PROVIDER: 'mock',
        SEARCH_PERSISTENCE_ENABLED: 'true',
        SEARCH_DATABASE_PATH: '../.tmp/e2e-searches.duckdb',
        DECISION_PERSISTENCE_ENABLED: 'true',
        DECISION_DATABASE_PATH: '../.tmp/e2e-decisions.duckdb',
        AI_ASSISTANT_ENABLED: 'true',
      },
    },
    { command: 'npm run dev -- --host 127.0.0.1', url: baseURL, reuseExistingServer: false, timeout: 120_000 },
  ],
  projects: [{ name: 'chromium', use: { ...devices['Desktop Chrome'] } }],
})

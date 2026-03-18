import { defineConfig, devices } from "@playwright/test";

const BACKEND_API_HOST = process.env.PW_BACKEND_API_HOST || "127.0.0.1";
const BACKEND_API_PORT = process.env.PW_BACKEND_API_PORT || "18000";
const BACKEND_HEALTH_URL = `http://${BACKEND_API_HOST}:${BACKEND_API_PORT}/health`;

export default defineConfig({
  testDir: "./tests/e2e",
  timeout: 30_000,
  expect: {
    timeout: 10_000,
  },
  reporter: [["list"], ["html", { open: "never" }]],
  fullyParallel: false,
  outputDir: "test-results/playwright",
  use: {
    baseURL: "http://localhost:3006",
    trace: "on-first-retry",
    screenshot: "only-on-failure",
    video: "retain-on-failure",
  },
  webServer: [
    {
      command: "npm run build && npm run start -- --port 3006",
      url: "http://localhost:3006",
      timeout: 240_000,
      reuseExistingServer: false,
    },
    {
      command: "python ../scripts/run_api_server.py",
      url: BACKEND_HEALTH_URL,
      timeout: 120_000,
      reuseExistingServer: true,
      env: {
        ...process.env,
        EPC_API_HOST: BACKEND_API_HOST,
        EPC_API_PORT: BACKEND_API_PORT,
      },
    },
  ],
  projects: [
    {
      name: "chromium",
      use: { ...devices["Desktop Chrome"] },
    },
  ],
});

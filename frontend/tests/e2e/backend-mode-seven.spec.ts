import { expect, test, type Page } from "@playwright/test";

const BACKEND_API_HOST = process.env.PW_BACKEND_API_HOST || "127.0.0.1";
const BACKEND_API_PORT = process.env.PW_BACKEND_API_PORT || "18000";
const BACKEND_API_PREFIX = `http://${BACKEND_API_HOST}:${BACKEND_API_PORT}`;

const DISCIPLINES = [
  "piping",
  "vessel",
  "rotating",
  "electrical",
  "instrumentation",
  "steel",
  "civil",
] as const;

async function configureBackendMode(page: Page) {
  await page.getByRole("button", { name: "Settings" }).click();
  const panel = page.locator("section").filter({ hasText: "Backend API Prefix" }).first();
  await panel.locator("select").first().selectOption("backend");
  await panel.getByPlaceholder("http://localhost:8000").fill(BACKEND_API_PREFIX);
}

for (const discipline of DISCIPLINES) {
  test(`backend mode calculation works for ${discipline}`, async ({ page }) => {
    await page.goto(`/${discipline}`);
    await configureBackendMode(page);

    await page.getByRole("button", { name: "Run Calculation" }).click();

    await expect(page.getByText("BACKEND").first()).toBeVisible();
    await expect(page.getByRole("heading", { name: "Request Error" })).toHaveCount(0);
    await expect(page.getByText(/SUCCESS|WARNING|성공|경고/i).first()).toBeVisible();
  });
}

import { expect, test } from "@playwright/test";

test("piping workbench smoke run", async ({ page }) => {
  await page.goto("/piping");

  await expect(page.getByRole("heading", { name: "Piping Integrity", exact: true })).toBeVisible();
  const responsePromise = page.waitForResponse((response) => response.url().includes("/api/calculate/piping") && response.ok());
  await page.getByRole("button", { name: "Run Calculation" }).click();
  await responsePromise;

  await expect(page.getByText("Step 1")).toBeVisible();
  await expect(page.getByText("AI Verification")).toBeVisible();
  await expect(page.getByText("Calculation Trace")).toBeVisible();
});

test("home to discipline navigation", async ({ page }) => {
  await page.goto("/");
  const pipingLink = page.locator('a[href="/piping"], a[href="/ko/piping"]').first();
  await expect(pipingLink).toBeVisible();
  await pipingLink.click();
  await expect(page).toHaveURL(/\/(ko\/)?piping$/);
});

import { expect, test } from "@playwright/test";

test("top bar preview shows empty state before run", async ({ page }) => {
  await page.setViewportSize({ width: 1600, height: 900 });
  await page.goto("/piping");

  await page.getByRole("button", { name: "Preview" }).click();
  await expect(page.getByText("Report Preview")).toBeVisible();
  await expect(page.getByText("No calculation result to preview.")).toBeVisible();
});

test("top bar JSON/MD export works after run", async ({ page }) => {
  await page.setViewportSize({ width: 1600, height: 900 });
  await page.goto("/piping");

  const responsePromise = page.waitForResponse((response) => response.url().includes("/api/calculate/piping") && response.ok());
  await page.getByRole("button", { name: "Run Calculation" }).click();
  await responsePromise;

  const jsonDownload = page.waitForEvent("download");
  await page.getByRole("button", { name: "JSON" }).click();
  const jsonFile = await jsonDownload;
  expect(jsonFile.suggestedFilename()).toMatch(/\.json$/i);

  const mdDownload = page.waitForEvent("download");
  await page.getByRole("button", { name: "MD" }).click();
  const mdFile = await mdDownload;
  expect(mdFile.suggestedFilename()).toMatch(/\.md$/i);
});

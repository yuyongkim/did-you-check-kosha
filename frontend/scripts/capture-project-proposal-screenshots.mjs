import { execSync, spawn } from "node:child_process";
import { mkdirSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { setTimeout as delay } from "node:timers/promises";
import { chromium, devices } from "@playwright/test";

const ROOT_DIR = resolve(process.cwd(), "..");
const OUTPUT_DIR = resolve(ROOT_DIR, "docs", "proposals", "assets", "project-intro", "screenshots");
const BASE_URL = "http://localhost:3012";

function ensureDir(path) {
  mkdirSync(path, { recursive: true });
}

async function isServerUp(url = BASE_URL) {
  try {
    const res = await fetch(url, { method: "GET" });
    return res.ok;
  } catch {
    return false;
  }
}

async function waitForServer(url = BASE_URL, timeoutMs = 180000) {
  const startedAt = Date.now();
  while (Date.now() - startedAt < timeoutMs) {
    if (await isServerUp(url)) return true;
    await delay(1500);
  }
  return false;
}

async function clickIfVisible(locator) {
  if (await locator.count()) {
    const target = locator.first();
    if (await target.isVisible()) {
      await target.click();
      return true;
    }
  }
  return false;
}

async function openSettings(page) {
  const clicked = await clickIfVisible(page.locator('button[title="Settings"]'))
    || await clickIfVisible(page.locator('button[title="설정"]'))
    || await clickIfVisible(page.getByRole("button", { name: /Settings|설정/ }));
  if (!clicked) {
    throw new Error("Cannot open settings panel.");
  }
  await page.waitForTimeout(400);
}

async function runCalculation(page, discipline) {
  await page.goto(`${BASE_URL}/${discipline}`, { waitUntil: "domcontentloaded" });
  await page.waitForLoadState("networkidle");

  const runButton = page.getByRole("button", { name: /Run Calculation|계산 실행/ }).first();
  await runButton.waitFor({ state: "visible", timeout: 15000 });

  const responsePromise = page.waitForResponse(
    (res) => res.url().includes(`/api/calculate/${discipline}`) && res.ok(),
    { timeout: 45000 },
  );

  await runButton.click();
  await responsePromise;
  await page.waitForTimeout(1200);
}

async function captureDesktopScreenshots(browser) {
  const context = await browser.newContext({
    viewport: { width: 1920, height: 1080 },
    deviceScaleFactor: 1,
  });
  const page = await context.newPage();

  await page.goto(`${BASE_URL}/`, { waitUntil: "domcontentloaded" });
  await page.waitForLoadState("networkidle");

  await page.screenshot({
    path: resolve(OUTPUT_DIR, "01_main_landing.png"),
    fullPage: false,
  });

  await openSettings(page);
  await page.screenshot({
    path: resolve(OUTPUT_DIR, "04_settings_panel.png"),
    fullPage: false,
  });

  // Close settings popup if needed
  await clickIfVisible(page.locator('button[title="Settings"]'));
  await page.waitForTimeout(300);

  await runCalculation(page, "piping");
  await page.screenshot({
    path: resolve(OUTPUT_DIR, "02_core_feature_piping.png"),
    fullPage: false,
  });

  await page.goto(`${BASE_URL}/`, { waitUntil: "domcontentloaded" });
  await page.waitForLoadState("networkidle");
  await page.screenshot({
    path: resolve(OUTPUT_DIR, "03_dashboard_management.png"),
    fullPage: false,
  });

  await runCalculation(page, "rotating");
  await page.screenshot({
    path: resolve(OUTPUT_DIR, "06_result_outcome_rotating.png"),
    fullPage: false,
  });

  await context.close();
}

async function captureMobileScreenshot(browser) {
  const context = await browser.newContext({
    ...devices["iPhone 12"],
  });
  const page = await context.newPage();

  await page.goto(`${BASE_URL}/rotating`, { waitUntil: "domcontentloaded" });
  await page.waitForLoadState("networkidle");
  await runCalculation(page, "rotating");
  await page.screenshot({
    path: resolve(OUTPUT_DIR, "05_mobile_responsive_rotating.png"),
    fullPage: false,
  });

  await context.close();
}

async function main() {
  ensureDir(OUTPUT_DIR);

  let serverProcess = null;
  let startedServerHere = false;

  if (!(await isServerUp())) {
    startedServerHere = true;
    const frontendDir = resolve(ROOT_DIR, "frontend");
    const logPath = resolve(frontendDir, "logs", "proposal_screenshot_capture.log");
    ensureDir(dirname(logPath));
    serverProcess = spawn("npm", ["run", "dev"], {
      cwd: frontendDir,
      stdio: "ignore",
      shell: true,
      detached: true,
    });
    serverProcess.unref();

    const up = await waitForServer();
    if (!up) {
      throw new Error("Frontend server did not start in time.");
    }
  }

  const browser = await chromium.launch({ headless: true });
  try {
    await captureDesktopScreenshots(browser);
    await captureMobileScreenshot(browser);
  } finally {
    await browser.close();
  }

  if (startedServerHere && serverProcess?.pid) {
    try {
      execSync(`taskkill /PID ${serverProcess.pid} /T /F`, { stdio: "ignore" });
    } catch {
      // Best effort cleanup
    }
  }

  console.log(`Saved screenshots to: ${OUTPUT_DIR}`);
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});

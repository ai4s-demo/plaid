import { chromium, Page } from "playwright";
import * as fs from "fs";
import * as path from "path";

const APP_URL = "https://dqeetww8lszcj.cloudfront.net/";
const OUTPUT_DIR = path.join(__dirname, "output");
const TIMESTAMPS_FILE = path.join(OUTPUT_DIR, "demo-timestamps.json");
const TEST_FILE = path.join(__dirname, "..", "test-case.xlsx");

const CHAT_MESSAGES = [
  "Generate a 96-well plate layout with 6 replicates per gene and 1 edge layer",
  "Can you redesign using a 384-well plate with 8 replicates and 2 edge layers?",
  "Use the first 10 genes with 8 replicates each, but give Gene25 20 replicates for dose-response study",
];

interface Timestamp {
  start: number;
  end: number;
}

let globalStart: number;
const timestamps: Record<string, Timestamp> = {};

function now(): number {
  return (Date.now() - globalStart) / 1000;
}

function sceneStart(id: string) {
  timestamps[id] = { start: now(), end: 0 };
}

function sceneEnd(id: string) {
  timestamps[id].end = now();
}

async function sleep(ms: number) {
  return new Promise((r) => setTimeout(r, ms));
}

async function typeInChat(page: Page, text: string) {
  const input = page.locator(".chat-input");
  await input.click();
  await input.type(text, { delay: 40 });
  await sleep(500);
  await page.locator(".btn-send").click();
}

async function waitForAIResponse(page: Page) {
  // Wait for typing indicator to appear
  await page.locator(".typing-indicator").waitFor({ state: "visible", timeout: 15000 }).catch(() => {});
  // Wait for it to disappear (AI finished)
  await page.locator(".typing-indicator").waitFor({ state: "detached", timeout: 120000 });
  await sleep(1000);
}

(async () => {
  fs.mkdirSync(OUTPUT_DIR, { recursive: true });

  const browser = await chromium.launch({
    headless: false,
    args: ["--window-size=1920,1080"],
  });

  const context = await browser.newContext({
    viewport: { width: 1920, height: 1080 },
    recordVideo: {
      dir: OUTPUT_DIR,
      size: { width: 1920, height: 1080 },
    },
  });

  const page = await context.newPage();
  globalStart = Date.now();

  // === Scene: login ===
  sceneStart("login");
  await page.goto(APP_URL, { waitUntil: "networkidle" });
  await sleep(2000);
  const usernameInput = page.locator('input[name="username"]');
  await usernameInput.click();
  await usernameInput.type("demouser", { delay: 60 });
  const passwordInput = page.locator('input[name="password"]');
  await passwordInput.click();
  await passwordInput.type("Demo@123", { delay: 60 });
  await sleep(500);
  await page.locator(".auth-form .btn-primary").click();
  await page.waitForSelector(".auth-form", { state: "detached", timeout: 15000 });
  await sleep(2000);
  sceneEnd("login");

  // === Scene: upload ===
  sceneStart("upload");
  const fileInput = page.locator("#file-input");
  await fileInput.setInputFiles(TEST_FILE);
  await page.locator(".source-info").waitFor({ state: "visible", timeout: 15000 });
  await sleep(8000); // Wait for narration to finish (~7.3s)
  sceneEnd("upload");

  // === Scene: chat_q1 ===
  sceneStart("chat_q1");
  await typeInChat(page, CHAT_MESSAGES[0]);
  await waitForAIResponse(page);
  // Expand layout and select it
  await page.locator(".layout-header").first().click().catch(() => {});
  await sleep(1000);
  await page.locator(".btn-select-layout").first().click().catch(() => {});
  await sleep(2000);
  sceneEnd("chat_q1");

  // === Scene: chat_q2 ===
  sceneStart("chat_q2");
  await typeInChat(page, CHAT_MESSAGES[1]);
  await waitForAIResponse(page);
  await page.locator(".layout-header").last().click().catch(() => {});
  await sleep(1000);
  await page.locator(".btn-select-layout").last().click().catch(() => {});
  await sleep(1000);
  // Scroll page up to show the plate layout
  await page.evaluate(() => window.scrollTo({ top: 0, behavior: "smooth" }));
  await sleep(2000);
  sceneEnd("chat_q2");

  // === Scene: chat_q3 ===
  sceneStart("chat_q3");
  await typeInChat(page, CHAT_MESSAGES[2]);
  await waitForAIResponse(page);
  await page.locator(".layout-header").last().click().catch(() => {});
  await sleep(1000);
  await page.locator(".btn-select-layout").last().click().catch(() => {});
  await sleep(1000);
  // Scroll page up to show the plate layout
  await page.evaluate(() => window.scrollTo({ top: 0, behavior: "smooth" }));
  await sleep(2000);
  sceneEnd("chat_q3");

  // === Scene: drag ===
  sceneStart("drag");
  await sleep(1000);
  // Find well elements in the plate SVG and drag one
  const wells = page.locator("svg g[data-well-id]");
  const wellCount = await wells.count();
  if (wellCount >= 2) {
    const srcBox = await wells.nth(0).boundingBox();
    const dstBox = await wells.nth(1).boundingBox();
    if (srcBox && dstBox) {
      const srcX = srcBox.x + srcBox.width / 2;
      const srcY = srcBox.y + srcBox.height / 2;
      const dstX = dstBox.x + dstBox.width / 2;
      const dstY = dstBox.y + dstBox.height / 2;
      await page.mouse.move(srcX, srcY);
      await page.mouse.down();
      await sleep(300);
      // Move in steps for visible drag effect
      const steps = 10;
      for (let i = 1; i <= steps; i++) {
        await page.mouse.move(
          srcX + ((dstX - srcX) * i) / steps,
          srcY + ((dstY - srcY) * i) / steps
        );
        await sleep(50);
      }
      await page.mouse.up();
    }
  }
  await sleep(6000); // Wait for narration to finish (~5.9s)
  sceneEnd("drag");

  // === Scene: export ===
  sceneStart("export");
  const downloadButtons = page.locator(".btn-download");
  for (let i = 0; i < 3; i++) {
    const btn = downloadButtons.nth(i);
    if ((await btn.count()) > 0) {
      await btn.click();
      await sleep(1500);
    }
  }
  await sleep(2000);
  sceneEnd("export");

  // Save timestamps
  fs.writeFileSync(TIMESTAMPS_FILE, JSON.stringify(timestamps, null, 2));
  console.log("Timestamps saved:", TIMESTAMPS_FILE);
  console.log(JSON.stringify(timestamps, null, 2));

  // Close browser - this finalizes the video
  await context.close();
  await browser.close();

  // Rename the recorded video
  const videos = fs.readdirSync(OUTPUT_DIR).filter((f) => f.endsWith(".webm"));
  if (videos.length > 0) {
    const src = path.join(OUTPUT_DIR, videos[videos.length - 1]);
    const dst = path.join(OUTPUT_DIR, "demo-video.webm");
    fs.renameSync(src, dst);
    console.log("Video saved:", dst);
  }
})();

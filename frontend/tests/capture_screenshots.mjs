// Captures UI screenshots of the running app for the poster and deck.
//   cd frontend && node tests/capture_screenshots.mjs
// Needs the backend on :8000 and the dev server on :3000 (npm run dev), and the demo clinician account.
import { chromium } from '@playwright/test';
import fs from 'node:fs';
import path from 'node:path';

const OUT = path.resolve('..', 'artifacts', 'ui');
fs.mkdirSync(OUT, { recursive: true });
const BASE = process.env.UI_BASE || 'http://localhost:3000';
const USER = process.env.UI_USER || 'clinician';
const PASS = process.env.UI_PASS || 'clinician123';

const browser = await chromium.launch({ channel: process.env.UI_CHANNEL || 'chrome' });   // installed Chrome; no browser download
const page = await (await browser.newContext({ viewport: { width: 1600, height: 1000 }, deviceScaleFactor: 1.5 })).newPage();
const shot = async (name, opts = {}) => { await page.screenshot({ path: path.join(OUT, name), ...opts }); console.log('saved', name); };

await page.goto(`${BASE}/login`);
await page.locator('input[type="text"]').waitFor();
await shot('ui_01_login.png');

await page.locator('input[type="text"]').fill(USER);
await page.locator('input[type="password"]').fill(PASS);
await page.locator('button[type="submit"]').click();
await page.waitForURL((u) => !u.pathname.includes('/login'), { timeout: 15000 });

await page.goto(`${BASE}/clinical/abpm-classifier`);
await page.getByRole('heading', { name: /ABPM Staging/ }).waitFor();
await page.getByRole('button', { name: /Simulated Normal/ }).waitFor();   // samples loaded
await shot('ui_02_abpm_empty.png');

for (const stage of ['Normal', 'Elevated', 'Stage 1', 'Stage 2']) {
  await page.getByRole('button', { name: `Simulated ${stage}` }).click();
  await page.getByRole('button', { name: /Classify record/ }).click();
  await page.getByRole('heading', { name: /Predicted stage/ }).waitFor({ timeout: 15000 });
  await page.waitForTimeout(900);                       // let the chart animation finish
  const flagged = await page.getByText(/manual clinician review recommended/).count();
  console.log(stage, 'review flag:', flagged > 0);
  await shot(`ui_03_abpm_${stage.replace(' ', '').toLowerCase()}.png`, { fullPage: true });
}
// Poster crop: narrower window and 2x scale, so the text stays legible when the image is printed small.
const ctx2 = await browser.newContext({ viewport: { width: 1200, height: 1000 }, deviceScaleFactor: 2 });
const p2 = await ctx2.newPage();
await p2.goto(`${BASE}/login`);
await p2.locator('input[type="text"]').fill(USER);
await p2.locator('input[type="password"]').fill(PASS);
await p2.locator('button[type="submit"]').click();
await p2.waitForURL((u) => !u.pathname.includes('/login'), { timeout: 15000 });
await p2.goto(`${BASE}/clinical/abpm-classifier`);
await p2.getByRole('button', { name: 'Simulated Stage 1' }).click();
await p2.getByRole('button', { name: /Classify record/ }).click();
await p2.getByRole('heading', { name: /Predicted stage/ }).waitFor({ timeout: 15000 });
await p2.waitForTimeout(900);
const card = await p2.getByRole('heading', { name: /Predicted stage/ }).locator('xpath=..').boundingBox();
const foot = await p2.getByText(/Decision support only/).boundingBox();
await p2.screenshot({ path: path.join(OUT, 'ui_poster_crop.png'), fullPage: true,
  clip: { x: card.x - 4, y: card.y - 4, width: card.width + 8, height: foot.y + foot.height - card.y + 8 } });
console.log('saved ui_poster_crop.png');
await browser.close();

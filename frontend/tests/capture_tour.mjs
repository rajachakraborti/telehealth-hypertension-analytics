// Three consistent-size screens for the poster's "product tour" strip: sign-in, data + summary statistics, dashboard.
//   cd frontend && node tests/capture_tour.mjs
import { chromium } from '@playwright/test';
import fs from 'node:fs';
import path from 'node:path';

const OUT = path.resolve('..', 'artifacts', 'ui', 'tour');
fs.mkdirSync(OUT, { recursive: true });
const BASE = process.env.UI_BASE || 'http://localhost:3000';
const DATA = path.resolve('..', 'backend', 'static', 'hypertension_sample.csv');
const browser = await chromium.launch({ channel: process.env.UI_CHANNEL || 'chrome' });
const page = await (await browser.newContext({ viewport: { width: 1300, height: 800 }, deviceScaleFactor: 2 })).newPage();
const W = 1180, H = 620;                                   // 1.9:1 clip of the main area (no sidebar)

await page.goto(`${BASE}/login`);
await page.locator('input[type="text"]').fill('clinician');          // typed so the shot shows a filled form
await page.locator('input[type="password"]').fill('clinician123');
await page.screenshot({ path: path.join(OUT, 'tour_1_login.png'), clip: { x: 0, y: 0, width: 1300, height: 765 } });
await page.locator('button[type="submit"]').click();
await page.waitForURL((u) => !u.pathname.includes('/login'), { timeout: 15000 });

// log in as admin for the data pages (same screens, any role may view them)
await page.getByRole('button', { name: /logout/i }).click();
await page.goto(`${BASE}/login`);
await page.locator('input[type="text"]').fill('admin');
await page.locator('input[type="password"]').fill('admin123');
await page.locator('button[type="submit"]').click();
await page.waitForURL((u) => !u.pathname.includes('/login'), { timeout: 15000 });

await page.goto(`${BASE}/data-ingestion/file-upload`);
await page.locator('input[type="file"]').setInputFiles(DATA);
await page.getByRole('button', { name: /upload file/i }).click();
await page.waitForTimeout(2000);
await page.goto(`${BASE}/data-exploration/summary-statistics`);
await page.waitForTimeout(2000);
await page.screenshot({ path: path.join(OUT, 'tour_2_summary.png'), clip: { x: 240, y: 62, width: 1050, height: 618 } });

await page.goto(`${BASE}/visualization/dashboard`);
await page.waitForTimeout(2500);
console.log('dashboard text:', (await page.locator('main').innerText()).replace(/\s+/g, ' ').slice(150, 330));
await page.screenshot({ path: path.join(OUT, 'tour_3_dashboard.png'), clip: { x: 240, y: 62, width: 1050, height: 618 } });
await browser.close();

// Captures every dashboard screen WITH a dataset loaded, running the clicks that produce results.
//   cd frontend && node tests/capture_all_pages.mjs        (backend on :8000, dev server on :3000)
import { chromium } from '@playwright/test';
import fs from 'node:fs';
import path from 'node:path';

const OUT = path.resolve('..', 'artifacts', 'ui', 'pages');
fs.rmSync(OUT, { recursive: true, force: true });
fs.mkdirSync(OUT, { recursive: true });
const BASE = process.env.UI_BASE || 'http://localhost:3000';
const DATA = path.resolve('..', 'backend', 'static', 'hypertension_sample.csv');

const browser = await chromium.launch({ channel: process.env.UI_CHANNEL || 'chrome' });
const page = await (await browser.newContext({ viewport: { width: 1500, height: 900 }, deviceScaleFactor: 1.5 })).newPage();
let n = 0;
const shot = async (label, route) => {
  const text = (await page.locator('main').first().innerText()).replace(/\s+/g, ' ');
  const empty = /no dataset loaded|please upload|upload a dataset|upload data/i.test(text);
  const bad = /failed to load|not found|error/i.test(text);
  const file = `${String(++n).padStart(2, '0')}_${label}.png`;
  await page.screenshot({ path: path.join(OUT, file) });
  console.log(`${file.padEnd(48)} ${bad ? 'ERROR-TEXT ' : empty ? 'EMPTY-STATE' : 'ok         '} ${route}`);
};
const go = async (route, wait = 1800) => { await page.goto(`${BASE}${route}`); await page.waitForTimeout(wait); };

// sign in (the sign-in screen itself first)
await page.goto(`${BASE}/login`);
await page.locator('input[type="text"]').fill('admin');
await page.locator('input[type="password"]').fill('admin123');
await page.screenshot({ path: path.join(OUT, `${String(++n).padStart(2, '0')}_login.png`) });
await page.locator('button[type="submit"]').click();
await page.waitForURL((u) => !u.pathname.includes('/login'), { timeout: 15000 });

// load a dataset through the UI, then every data page has something to show
await go('/data-ingestion/file-upload');
await page.locator('input[type="file"]').setInputFiles(DATA);
await page.getByRole('button', { name: /upload file/i }).click();
await page.waitForTimeout(2500);
await shot('data-upload', '/data-ingestion/file-upload');

await go('/data-ingestion/url-import'); await shot('data-url-import', '/data-ingestion/url-import');
await go('/data-exploration/summary-statistics'); await shot('explore-summary-statistics', '/data-exploration/summary-statistics');
await go('/data-exploration/data-table'); await shot('explore-data-table', '/data-exploration/data-table');
await go('/data-exploration/correlation-matrix'); await shot('explore-correlation-matrix', '/data-exploration/correlation-matrix');

await go('/data-cleaning/outlier-detection');
await page.getByRole('button', { name: /detect outliers/i }).click();
await page.waitForTimeout(2500);
await shot('cleaning-outlier-detection', '/data-cleaning/outlier-detection');
await go('/data-cleaning/imputation'); await shot('cleaning-imputation', '/data-cleaning/imputation');
await go('/data-cleaning/preprocessing-history'); await shot('cleaning-preprocessing-history', '/data-cleaning/preprocessing-history');

await go('/visualization/chart-builder');
const selects = page.locator('select');
await selects.nth(1).selectOption({ label: 'Age' });
await selects.nth(2).selectOption({ label: 'SystolicBP' });
await page.waitForTimeout(1500);
await shot('viz-chart-builder', '/visualization/chart-builder');
await go('/visualization/dashboard', 2500); await shot('viz-dashboard-risk', '/visualization/dashboard');
await go('/visualization/risk-gauge', 2500); await shot('viz-risk-gauge', '/visualization/risk-gauge');

await go('/modeling/model-selection'); await shot('modeling-model-training', '/modeling/model-selection');
await go('/modeling/hyperparameter-tuning'); await shot('modeling-hyperparameter-tuning', '/modeling/hyperparameter-tuning');
await go('/modeling/feature-importance'); await shot('modeling-feature-importance', '/modeling/feature-importance');

await go('/reporting/report-generator'); await shot('reporting-report-generator', '/reporting/report-generator');
await go('/reporting/export-options'); await shot('reporting-export-options', '/reporting/export-options');
await go('/pipeline/workflow-visualizer'); await shot('pipeline-workflow', '/pipeline/workflow-visualizer');
await go('/pipeline/pipeline-controls'); await shot('pipeline-controls', '/pipeline/pipeline-controls');
await go('/user-management/role-management'); await shot('user-role-management', '/user-management/role-management');
await go('/help'); await shot('help', '/help');

// the clinical page: classify one record and capture the result
await go('/clinical/abpm-classifier');
await page.getByRole('button', { name: 'Simulated Stage 1' }).click();
await page.getByRole('button', { name: /classify record/i }).click();
await page.getByRole('heading', { name: /predicted stage/i }).waitFor({ timeout: 15000 });
await page.waitForTimeout(1000);
await shot('clinical-abpm-staging-result', '/clinical/abpm-classifier');
await browser.close();

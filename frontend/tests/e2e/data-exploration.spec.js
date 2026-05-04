import { test, expect } from './auth.fixture.js';

async function openSection(page, sectionName) {
  await page.locator('.sidebar').getByText(sectionName).click();
}

test.describe('Data Exploration (authenticated)', () => {
  test('Summary Statistics page is reachable via sidebar', async ({ authenticatedPage }) => {
    await openSection(authenticatedPage, 'Data Exploration');
    await authenticatedPage.getByRole('link', { name: 'Summary Statistics' }).click();
    await expect(authenticatedPage).toHaveURL(/summary-statistics/);
  });

  test('Data Table page is reachable via sidebar', async ({ authenticatedPage }) => {
    await openSection(authenticatedPage, 'Data Exploration');
    await authenticatedPage.getByRole('link', { name: 'Data Table' }).click();
    await expect(authenticatedPage).toHaveURL(/data-table/);
  });

  test('Correlation Matrix page is reachable via sidebar', async ({ authenticatedPage }) => {
    await openSection(authenticatedPage, 'Data Exploration');
    await authenticatedPage.getByRole('link', { name: 'Correlation Matrix' }).click();
    await expect(authenticatedPage).toHaveURL(/correlation-matrix/);
  });
});

test.describe('Data Cleaning (authenticated)', () => {
  test('Imputation page is reachable via sidebar', async ({ authenticatedPage }) => {
    await openSection(authenticatedPage, 'Data Cleaning');
    await authenticatedPage.getByRole('link', { name: 'Imputation' }).click();
    await expect(authenticatedPage).toHaveURL(/imputation/);
  });

  test('Outlier Detection page is reachable via sidebar', async ({ authenticatedPage }) => {
    await openSection(authenticatedPage, 'Data Cleaning');
    await authenticatedPage.getByRole('link', { name: 'Outlier Detection' }).click();
    await expect(authenticatedPage).toHaveURL(/outlier-detection/);
  });
});

test.describe('Modeling (authenticated)', () => {
  test('Model Selection page is reachable via sidebar', async ({ authenticatedPage }) => {
    await openSection(authenticatedPage, 'Modeling');
    await authenticatedPage.getByRole('link', { name: 'Model Selection' }).click();
    await expect(authenticatedPage).toHaveURL(/model-selection/);
  });

  test('Hyperparameter Tuning page is reachable via sidebar', async ({ authenticatedPage }) => {
    await openSection(authenticatedPage, 'Modeling');
    await authenticatedPage.getByRole('link', { name: 'Hyperparameter Tuning' }).click();
    await expect(authenticatedPage).toHaveURL(/hyperparameter-tuning/);
  });
});

test.describe('Visualization (authenticated)', () => {
  test('Dashboard is reachable via sidebar', async ({ authenticatedPage }) => {
    await openSection(authenticatedPage, 'Visualization');
    await authenticatedPage.getByRole('link', { name: 'Dashboard' }).click();
    await expect(authenticatedPage).toHaveURL(/dashboard/);
  });

  test('Risk Gauge page is reachable via sidebar', async ({ authenticatedPage }) => {
    await openSection(authenticatedPage, 'Visualization');
    await authenticatedPage.getByRole('link', { name: 'Risk Gauge' }).click();
    await expect(authenticatedPage).toHaveURL(/risk-gauge/);
  });
});

test.describe('Reporting (authenticated)', () => {
  test('Report Generator page is reachable via sidebar', async ({ authenticatedPage }) => {
    await openSection(authenticatedPage, 'Reporting');
    await authenticatedPage.getByRole('link', { name: 'Generate Report' }).click();
    await expect(authenticatedPage).toHaveURL(/report-generator/);
  });
});

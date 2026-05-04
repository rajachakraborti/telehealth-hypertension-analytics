import { test, expect } from './auth.fixture.js';

test.describe('Sidebar Navigation (authenticated)', () => {
  test('sidebar is visible when logged in', async ({ authenticatedPage }) => {
    await expect(authenticatedPage.locator('.sidebar')).toBeVisible();
  });

  test('sidebar is hidden when not logged in', async ({ page }) => {
    await page.goto('/login');
    await expect(page.locator('.sidebar')).not.toBeVisible();
  });

  test('sidebar contains all top-level menu sections', async ({ authenticatedPage }) => {
    const sidebar = authenticatedPage.locator('.sidebar');
    const sections = [
      'Data Ingestion',
      'Data Exploration',
      'Data Cleaning',
      'Modeling',
      'Visualization',
      'Reporting',
      'Pipeline',
      'User Management',
      'Help & Support',
    ];
    for (const section of sections) {
      await expect(sidebar).toContainText(section);
    }
  });

  test('clicking Data Ingestion expands its sub-links', async ({ authenticatedPage }) => {
    await authenticatedPage.locator('.sidebar').getByText('Data Ingestion').click();
    await expect(authenticatedPage.getByRole('link', { name: 'File Upload' })).toBeVisible();
    await expect(authenticatedPage.getByRole('link', { name: 'URL Import' })).toBeVisible();
  });

  test('clicking an expanded section again collapses it', async ({ authenticatedPage }) => {
    const toggle = authenticatedPage.locator('.sidebar').getByText('Data Ingestion');
    await toggle.click();
    await expect(authenticatedPage.getByRole('link', { name: 'File Upload' })).toBeVisible();
    await toggle.click();
    await expect(authenticatedPage.getByRole('link', { name: 'File Upload' })).not.toBeVisible();
  });

  test('clicking File Upload navigates to the correct page', async ({ authenticatedPage }) => {
    await authenticatedPage.locator('.sidebar').getByText('Data Ingestion').click();
    await authenticatedPage.getByRole('link', { name: 'File Upload' }).click();
    await expect(authenticatedPage).toHaveURL(/data-ingestion\/file-upload/);
  });

  test('clicking Modeling expands its sub-links', async ({ authenticatedPage }) => {
    await authenticatedPage.locator('.sidebar').getByText('Modeling').click();
    await expect(authenticatedPage.getByRole('link', { name: 'Model Selection' })).toBeVisible();
    await expect(authenticatedPage.getByRole('link', { name: 'Hyperparameter Tuning' })).toBeVisible();
    await expect(authenticatedPage.getByRole('link', { name: 'Feature Importance' })).toBeVisible();
  });

  test('Help link navigates to documentation page', async ({ authenticatedPage }) => {
    await authenticatedPage.locator('.sidebar').getByText('Help & Support').click();
    await authenticatedPage.getByRole('link', { name: 'Documentation' }).click();
    await expect(authenticatedPage).toHaveURL(/help/);
  });
});

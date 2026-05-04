import { test, expect } from '@playwright/test';

test.describe('Public Pages', () => {
  test('login page renders all form elements', async ({ page }) => {
    await page.goto('/login');
    await expect(page.locator('h2')).toContainText('Login');
    await expect(page.locator('input[type="text"]')).toBeVisible();
    await expect(page.locator('input[type="password"]')).toBeVisible();
    await expect(page.locator('button[type="submit"]')).toContainText('Login');
  });

  test('login page has a link to the register page', async ({ page }) => {
    await page.goto('/login');
    const registerLink = page.getByRole('link', { name: 'Register' });
    await expect(registerLink).toBeVisible();
    await registerLink.click();
    await expect(page).toHaveURL(/register/);
  });

  test('register page is accessible from the login page', async ({ page }) => {
    await page.goto('/register');
    await expect(page).toHaveURL(/register/);
    // Page should not redirect unauthenticated users
    await expect(page).not.toHaveURL(/login/);
  });

  test('help page is accessible without being logged in', async ({ page }) => {
    await page.goto('/help');
    await expect(page).toHaveURL(/help/);
    await expect(page).not.toHaveURL(/login/);
  });

  test('root route redirects to login when unauthenticated', async ({ page }) => {
    await page.goto('/');
    await expect(page).toHaveURL(/login/);
  });

  test('protected data-ingestion route redirects to login when unauthenticated', async ({ page }) => {
    await page.goto('/data-ingestion/file-upload');
    await expect(page).toHaveURL(/login/);
  });

  test('protected modeling route redirects to login when unauthenticated', async ({ page }) => {
    await page.goto('/modeling/model-selection');
    await expect(page).toHaveURL(/login/);
  });
});

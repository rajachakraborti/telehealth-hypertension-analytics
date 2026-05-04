import { test, expect } from '@playwright/test';

test.describe('Authentication Flows', () => {
  test('login form shows an error message on invalid credentials', async ({ page }) => {
    await page.route('**/api/auth/login', route =>
      route.fulfill({
        status: 400,
        contentType: 'application/json',
        body: JSON.stringify({ detail: 'Invalid username or password' }),
      })
    );

    await page.goto('/login');
    await page.locator('input[type="text"]').fill('wronguser');
    await page.locator('input[type="password"]').fill('wrongpass');
    await page.locator('button[type="submit"]').click();

    await expect(page.getByText('Invalid username or password')).toBeVisible();
  });

  test('login button shows loading state while the request is in flight', async ({ page }) => {
    await page.route('**/api/auth/login', async route => {
      await page.waitForTimeout(600);
      await route.fulfill({
        status: 400,
        contentType: 'application/json',
        body: JSON.stringify({ detail: 'Invalid credentials' }),
      });
    });

    await page.goto('/login');
    await page.locator('input[type="text"]').fill('testuser');
    await page.locator('input[type="password"]').fill('testpass');
    await page.locator('button[type="submit"]').click();

    await expect(page.locator('button[type="submit"]')).toContainText('Logging in...');
    await expect(page.locator('button[type="submit"]')).toBeDisabled();
  });

  test('successful login redirects to the dashboard', async ({ page }) => {
    await page.route('**/api/auth/login', route =>
      route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({ access_token: 'mock-token', token_type: 'bearer' }),
      })
    );
    await page.route('**/api/auth/users/me', route =>
      route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({ id: 1, username: 'testuser' }),
      })
    );

    await page.goto('/login');
    await page.locator('input[type="text"]').fill('testuser');
    await page.locator('input[type="password"]').fill('testpass123');
    await page.locator('button[type="submit"]').click();

    await expect(page).toHaveURL('http://localhost:3000/');
    await expect(page.locator('.sidebar')).toBeVisible();
  });

  test('username and password fields are required', async ({ page }) => {
    await page.goto('/login');
    await page.locator('button[type="submit"]').click();

    const usernameInput = page.locator('input[type="text"]');
    const isValid = await usernameInput.evaluate(el => el.validity.valid);
    expect(isValid).toBe(false);
  });

  test('logging out clears the session and returns to login', async ({ page }) => {
    // Set up authenticated state
    await page.route('**/api/auth/users/me', route =>
      route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({ id: 1, username: 'testuser' }),
      })
    );
    await page.goto('/login');
    await page.evaluate(() => localStorage.setItem('token', 'mock-token'));
    await page.goto('/');
    await expect(page.locator('.sidebar')).toBeVisible();

    // Find and click logout
    const header = page.locator('header');
    await header.getByRole('button', { name: /logout/i }).click();

    await expect(page).toHaveURL(/login/);
    const token = await page.evaluate(() => localStorage.getItem('token'));
    expect(token).toBeNull();
  });
});

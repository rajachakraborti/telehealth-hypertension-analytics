import { test as base } from '@playwright/test';

export { expect } from '@playwright/test';

export const MOCK_USER = {
  id: 1,
  username: 'testuser',
  email: 'testuser@example.com',
  role: 'clinician',
};
export const MOCK_TOKEN = 'mock-jwt-token-for-e2e-testing';

/**
 * Extends the base test with an `authenticatedPage` fixture.
 * Mocks only the auth endpoints (/api/auth/login and /api/auth/users/me)
 * so tests work without a running database. All other API calls go to the
 * real backend at http://localhost:8000.
 */
export const test = base.extend({
  authenticatedPage: async ({ page }, use) => {
    // Intercept auth endpoints — database not required for these mocks
    await page.route('**/api/auth/users/me', route =>
      route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify(MOCK_USER),
      })
    );
    await page.route('**/api/auth/login', route =>
      route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({ access_token: MOCK_TOKEN, token_type: 'bearer' }),
      })
    );

    // Seed token so AuthContext initialises as logged-in
    await page.goto('/login');
    await page.evaluate(token => localStorage.setItem('token', token), MOCK_TOKEN);
    await page.goto('/');

    await use(page);

    // Clean up
    await page.evaluate(() => localStorage.removeItem('token'));
  },
});

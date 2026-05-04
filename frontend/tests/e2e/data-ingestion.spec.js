import { test, expect } from './auth.fixture.js';

const CSV_CONTENT = 'systolic,diastolic,age\n130,85,45\n140,90,50\n150,95,60';

async function goToFileUpload(page) {
  await page.locator('.sidebar').getByText('Data Ingestion').click();
  await page.getByRole('link', { name: 'File Upload' }).click();
  await expect(page).toHaveURL(/file-upload/);
}

test.describe('File Upload (authenticated, real backend)', () => {
  test('page renders heading, file input, and upload button', async ({ authenticatedPage }) => {
    await goToFileUpload(authenticatedPage);
    await expect(authenticatedPage.getByRole('heading', { name: 'Upload Data File' })).toBeVisible();
    await expect(authenticatedPage.locator('input[type="file"]')).toBeVisible();
    await expect(authenticatedPage.locator('button[type="submit"]')).toBeVisible();
  });

  test('upload button is disabled before a file is selected', async ({ authenticatedPage }) => {
    await goToFileUpload(authenticatedPage);
    await expect(authenticatedPage.locator('button[type="submit"]')).toBeDisabled();
  });

  test('selecting a file enables the upload button', async ({ authenticatedPage }) => {
    await goToFileUpload(authenticatedPage);
    await authenticatedPage.locator('input[type="file"]').setInputFiles({
      name: 'sample.csv',
      mimeType: 'text/csv',
      buffer: Buffer.from(CSV_CONTENT),
    });
    await expect(authenticatedPage.locator('button[type="submit"]')).toBeEnabled();
  });

  test('uploading a valid CSV shows success message', async ({ authenticatedPage }) => {
    await goToFileUpload(authenticatedPage);
    await authenticatedPage.locator('input[type="file"]').setInputFiles({
      name: 'sample.csv',
      mimeType: 'text/csv',
      buffer: Buffer.from(CSV_CONTENT),
    });
    await authenticatedPage.locator('button[type="submit"]').click();
    await expect(authenticatedPage.getByText('File uploaded successfully!')).toBeVisible({
      timeout: 10_000,
    });
  });

  test('uploading an invalid file type shows error message', async ({ authenticatedPage }) => {
    await goToFileUpload(authenticatedPage);
    await authenticatedPage.locator('input[type="file"]').setInputFiles({
      name: 'notes.txt',
      mimeType: 'text/plain',
      buffer: Buffer.from('this is not a data file'),
    });
    await authenticatedPage.locator('button[type="submit"]').click();
    await expect(
      authenticatedPage.locator('p').filter({ hasText: /error|invalid/i })
    ).toBeVisible({ timeout: 10_000 });
  });

  test('supported formats label is shown in the upload area', async ({ authenticatedPage }) => {
    await goToFileUpload(authenticatedPage);
    await expect(authenticatedPage.getByText(/CSV, Excel/i)).toBeVisible();
  });
});

test.describe('URL Import (authenticated)', () => {
  test('URL Import page is reachable via sidebar', async ({ authenticatedPage }) => {
    await authenticatedPage.locator('.sidebar').getByText('Data Ingestion').click();
    await authenticatedPage.getByRole('link', { name: 'URL Import' }).click();
    await expect(authenticatedPage).toHaveURL(/url-import/);
  });
});

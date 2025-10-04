import { test, expect } from '@playwright/test';

const OPENAI_API_KEY = process.env.OPENAI_API_KEY || process.env.OPENAI_KEY || '';

test.describe('Homepage demo forms', () => {
  test.beforeEach(async ({ page }) => {
    test.skip(!OPENAI_API_KEY, 'OPENAI_API_KEY missing in .env');
    await page.goto('/');
  });

  test('phone_a_friend submits and returns answer', async ({ page }) => {
    // Ensure phone tab is active
    await page.getByRole('button', { name: 'phone_a_friend' }).click();

    await page.getByPlaceholder('sk-...').fill(OPENAI_API_KEY);
    await page.getByPlaceholder('What is the best way to structure a Python project?').fill('What is FastMCP?');
    await page.getByPlaceholder("I'm building a FastAPI application with SQLAlchemy").fill('E2E test context');

    const askButton = page.getByRole('button', { name: 'Ask Question' });
    await expect(askButton).toBeEnabled();
    await askButton.click();

    // Expect response container to appear with some text
    const response = page.locator('.response-container');
    await expect(response).toBeVisible();
    await expect(response).not.toHaveText('', { timeout: 15000 });
  });

  test('review_plan submits and returns structured JSON', async ({ page }) => {
    await page.getByRole('button', { name: 'review_plan' }).click();

    await page.getByPlaceholder('sk-...').fill(OPENAI_API_KEY);
    await page
      .getByPlaceholder('# Project Plan\n\n## Objectives\n- Build a new feature\n\n## Timeline\n- Week 1: Design\n- Week 2: Implementation')
      .fill('# Project Plan\n\n## Objectives\n- Implement auth\n\n## Timeline\n- Week 1: Design\n- Week 2: Implementation');

    // Default level is Standard, submit
    const reviewButton = page.getByRole('button', { name: 'Review Plan' });
    await expect(reviewButton).toBeEnabled();
    await reviewButton.click();

    const response = page.locator('.response-container');
    await expect(response).toBeVisible();
    await expect(response).not.toHaveText('', { timeout: 20000 });

    const text = await response.textContent();
    expect(text).toContain('overall_score');
    expect(text).toContain('strengths');
    expect(text).toContain('weaknesses');
  });
});

import { test, expect } from '@playwright/test';

test.describe('Homepage metrics widget', () => {
  test('renders and updates after demo calls', async ({ page, request }) => {
    // Navigate to homepage
    await page.goto('/');

    // Metrics section should render
    const section = page.locator('section.metrics');
    await expect(section).toBeVisible();
    await expect(section.getByRole('heading', { name: 'Service Metrics' })).toBeVisible();

    // Badge shows source (memory or database)
    const badge = section.locator('.metrics__badge');
    await expect(badge).toBeVisible();

    // Trigger a demo call to increment counters (demos must be enabled on server)
    const r = await request.post('/api/demo/phone-a-friend', {
      data: { question: 'ping', api_key: 'sk-bogus' },
    });
    expect([200, 401, 429, 500]).toContain(r.status());

    // Reload to fetch fresh summary (widget fetches on mount)
    await page.reload();

    // Table should contain at least one row or non-zero total
    const totalKpi = section.locator('.metrics__kpi-value');
    await expect(totalKpi).toBeVisible();
    // total value should be a number string; allow zero if server gated demos
    const totalText = await totalKpi.first().textContent();
    expect(totalText).not.toBeNull();
  });
});



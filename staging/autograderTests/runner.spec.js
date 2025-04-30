import { test, expect } from '@playwright/test';

test.beforeEach(async ({page}) => {
    await page.goto('http://localhost:3000');
});

test.describe('Test p5.js sketch', () => {
    test('Submission is in the expected format', async ({page}) => {
        const canvasCount = await page.locator('css=canvas').count();
        expect(canvasCount).toBe(1);
    });

    test('Run output tests', async ({page}) => {
        await expect(page.locator('#test-status')).toHaveText("complete");
        const testResults = await page.evaluate(() => window.results);
        await expect(testResults).toBeTruthy();
        if (testResults) {
            for (const res of testResults) {
                test.step(res.message, () => {
                    expect(res.status).toBe("passed");
                })
            }
        }
        // Need to convert testResults to JSON in Gradescope format
    })
});
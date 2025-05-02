import { test, expect } from '@playwright/test';

// This should contain the entry points (i.e. the index.html page) for all sketches to be tested.
// sketchName is the name of the sketch displayed in the test results that students
// URLs are relative to the staging folder, not the autograderTests folder.
const SKETCH_ENTRY_POINTS = [
    // {
    //     sketchName: 'p5.js sketch',
    //     url: '/singleSketch/index.html'
    // },
    {
        sketchName: 'sketch 1',
        url: '/multiSketch/sketch1/index.html'
    },
    {
        sketchName: 'sketch 2',
        url: '/multiSketch/sketch2/index.html'
    }
]

for (const sketch of SKETCH_ENTRY_POINTS) {
    test.describe(`Test ${sketch.sketchName}`, () => {
        test('Submission is in the expected format', async ({page}) => {
            await page.goto(sketch.url);
            const canvasCount = await page.locator('css=canvas').count();
            expect(canvasCount).toBe(1);
        });
    
        test('Run output tests', async ({page}) => {
            await page.goto(sketch.url);
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
        })
    });
}

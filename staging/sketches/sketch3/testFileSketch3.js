import { substituteDraw, TestResults, advanceToFrame, getShapes, canvasStatus, testSettingIsCalled, LOAD_IMAGE, checkCanvasSize, TestImage } from "../../testingDependencies/test-utils.js";

/*** EXERCISE-SPECIFIC TEST FUNCTIONS. These functions are called from runTests() below. */
function checkImageProperties(expectedImg, actualShapes) {
    const actualImgs = actualShapes.filter(s => s.type === IMAGE);
    if (actualImgs.length === 0) {
        TestResults.addFail(`At frame ${frameCount}, no images were found on the canvas.`);
    } else {
        const lastImg = actualImgs[actualImgs.length - 1];
        if (expectedImg.isEqualTo(lastImg)) {
            TestResults.addPass(`At frame ${frameCount}, the image is displayed in the centre with a width of ${lastImg.w} and a height of ${lastImg.h}.`);
        } else {
            TestResults.addFail(`At frame ${frameCount}, expected the image to be displayed in the centre with a width of ${expectedImg.w} and a height of ${expectedImg.h}. Found an image at ${lastImg.x}, ${lastImg.y} (coordinates converted to CORNER mode), with a width of ${lastImg.w} and a height of ${lastImg.h}.`);
        }
    }
}

/*** END EXERCISE-SPECIFIC TEST FUNCTIONS */

/** REQUIRED FUNCTIONS - DO NOT EDIT */

/**
 * A hacky way to wait for p5js to load the canvas. Include in all exercise test files.
 */
function waitForP5() {
    const canvases = document.getElementsByTagName("canvas");
    if (canvases.length > 0) { // p5.js has loaded i.e. drawn a canvas
        clearInterval(loadTimer); // Stop the timer
        canvases[0].style.pointerEvents = "none"; // prevents p5.js from responding to mouse events independent of the tests
        substituteDraw(); 
        for (const e of canvasStatus.errors) {
            TestResults.addFail(`In frame ${frameCount}, ${e}`);
        }
        runTests(canvases[0]); // Run the tests below
    }
}

/**
 * For use with Playwright. 
 * Makes the relevant contents of the TestResults instance available to Playwright.
 */
function completeTests() {
    window.results = TestResults.playwright;
    document.getElementById("test-status").innerText = "complete";
}

/**
 * Run all tests.
 * @param {HTMLElement} canvas The HTML canvas created by p5.js
 */
async function runTests(canvas) {

    // YOUR TESTS HERE. Write unit test functions then use TestResults static methods to show test results e.g.:
    // Tests can take any format but they must end by storing either a pass or a fail in the TestResults instance as shown below.
    // The messages passed to addPass / addFail will be displayed to the student.
    // TestResults.addPass("This test passed.");
    // TestResults.addFail("This test failed.");
    // TestResults.addWarning("This is a warning.");

    // Some common tests are already defined in ../testingDependencies/test-utils.js e.g.:
    checkCanvasSize(512, 410);
    // Some of these tests, like checkCanvasSize already store the result in TestResults so you do not have to specify feedback.
    // To write tests, you should have a good understanding of automated software testing.
    // If you don't, here is an overview https://www.geeksforgeeks.org/automation-testing-software-testing/

    const loadInPreload = testSettingIsCalled(LOAD_IMAGE, false, false, true);
    const loadInSetup = testSettingIsCalled(LOAD_IMAGE, true, false, false);
    const loadInDraw = testSettingIsCalled(LOAD_IMAGE, false, true, false);
    if (loadInPreload) {
        TestResults.addPass("<code>loadImage()</code> is called in <code>preload()</code>.");
    }
    if (loadInSetup) {
        TestResults.addWarning("<code>loadImage()</code> is called in <code>setup()</code>. Although this can work, it should only be called in <code>preload()</code> to ensure the image is fully loaded before any other code is run.");
    }
    if (loadInDraw) {
        TestResults.addFail("<code>loadImage()</code> should not be called in <code>draw()</code> because it will repeatedly load the image.");
    }
    if (!loadInPreload && !loadInSetup && !loadInDraw) {
        TestResults.addWarning("<code>loadImage()</code> does not appear to be called (this test will not detect usage of <code>loadImage()</code> outside <code>preload()</code>, <code>setup()</code>, or <code>draw()</code>).");
    }
    const imgOnLoad = new TestImage(width / 2, height / 2, width, height, 1024, 820, CENTER);
    checkImageProperties(imgOnLoad, [...getShapes()]);
    imgOnLoad.x -= 0.5;
    imgOnLoad.y -= 0.5;
    imgOnLoad.w++;
    imgOnLoad.h++;
    advanceToFrame(frameCount+1);
    checkImageProperties(imgOnLoad, [...getShapes()]);
    advanceToFrame(1000);
    imgOnLoad.x = width / 2 - 922 / 2;
    imgOnLoad.y = height / 2 - 820 / 2;
    imgOnLoad.w = 922;
    imgOnLoad.h = 820;
    checkImageProperties(imgOnLoad, [...getShapes()]);

    // DO NOT EDIT This statement must be last - makes test results available to Playwright
    completeTests();
}

// Calls waitForP5() every half second until p5.js finishes loading
const loadTimer = setInterval(waitForP5, 500);
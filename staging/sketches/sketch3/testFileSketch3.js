import { substituteDraw, TestResults, advanceToFrame, getShapes, canvasStatus, testSettingIsCalled, LOAD_IMAGE, checkCanvasSize, TestImage } from "https://cdn.jsdelivr.net/gh/Supportive-IDE/p5js-testing-demo@latest/p5jsTestingLibrary.js";

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
        // substituteDraw(); 
        for (const e of canvasStatus.errors) {
            TestResults.addFail(`In frame ${frameCount}, ${e}`);
        }
        runTests(canvases[0]); // Run the tests below
    }
}

/**
 * For use with Playwright. 
 * Makes the relevant contents of the TestResults instance available to Playwright and sets the visibility of the tests for Gradescope.
 * @param {boolean} [visibility=false] Whether or not the test outputs should be visible to students in Gradescope
 */
function completeTests(visibility = false) {
    window.results = TestResults.playwright; 
    document.getElementById("test-status").innerText = "complete";
    document.getElementById("test-visibility").innerText = visibility ? "visible" : "hidden";
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
    
    // Some of these tests, like checkCanvasSize already store the result in TestResults so you do not have to specify feedback.
    // To write tests, you should have a good understanding of automated software testing.
    // If you don't, here is an overview https://www.geeksforgeeks.org/automation-testing-software-testing/
    
    const loadInSetup = testSettingIsCalled(LOAD_IMAGE.re, true, false);
    const loadInDraw = testSettingIsCalled(LOAD_IMAGE.re, false, true);
    if (loadInSetup) {
        TestResults.addPass("<code>loadImage()</code> is called in setup().");
    }
    if (loadInDraw) {
        TestResults.addFail("<code>loadImage()</code> should not be called in <code>draw()</code> because it will repeatedly load the image.");
    }
    if (!loadInSetup && !loadInDraw) {
        TestResults.addFail("<code>loadImage()</code> does not appear to be called (this test will not detect usage of <code>loadImage()</code> outside <code>setup()</code> or <code>draw()</code>).");
    }
    await advanceToFrame(1)
    checkCanvasSize(512, 410);
    TestResults.addPass(`Frame count is ${frameCount}`)
    const imgOnLoad = new TestImage(width / 2, height / 2, width, height, 1024, 820, CENTER);
    checkImageProperties(imgOnLoad, [...getShapes()]);
    imgOnLoad.x -= 0.5;
    imgOnLoad.y -= 0.5;
    imgOnLoad.w++;
    imgOnLoad.h++;
    await advanceToFrame(frameCount+1);
    checkImageProperties(imgOnLoad, [...getShapes()]);
    await advanceToFrame(1000);
    imgOnLoad.x = width / 2 - 922 / 2;
    imgOnLoad.y = height / 2 - 820 / 2;
    imgOnLoad.w = 922;
    imgOnLoad.h = 820;
    checkImageProperties(imgOnLoad, [...getShapes()]);

    // DO NOT DELETE This statement must be last - makes test results available to Playwright
    // pass true to completeTests() to make test output visible to students in Gradescope
    completeTests(true);
}

// Calls waitForP5() every half second until p5.js finishes loading
const loadTimer = setInterval(waitForP5, 500);
import { TestResults, canvasStatus, substituteDraw, checkCanvasSize, checkShapes, getShapes, TestSquare } from "../../testingDependencies/test-utils.js";

/*** EXERCISE-SPECIFIC TEST FUNCTIONS. These functions are called from runTests() below. */


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
    checkCanvasSize(400, 400);
    // Some of these tests, like checkCanvasSize already store the result in TestResults so you do not have to specify feedback.
    // To write tests, you should have a good understanding of automated software testing.
    // If you don't, here is an overview https://www.geeksforgeeks.org/automation-testing-software-testing/

    const shapes = getShapes();
    const square = new TestSquare(200, 200, 50);
    checkShapes([square], shapes, false, false);

    // DO NOT DELETE This statement must be last - makes test results available to Playwright
    // pass true to completeTests() to make test output visible to students in Gradescope
    completeTests(true);
}

// Calls waitForP5() every half second until p5.js finishes loading
const loadTimer = setInterval(waitForP5, 500);
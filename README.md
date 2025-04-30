# Repo Contents

This autograder template was created using [this Jest autograder](https://github.com/ucsb-gradescope-tools/jest-autograder) as a reference.

**Important:** Do not edit / move / rename any files EXCEPT for testFile.js and sketch.js in the staging folder.

Description of repo contents: 
- localautograder folder: Can be ignored and will probably be removed.
- staging folder: This is where the testing happens. Do not edit any files (or change any file names) EXCEPT for testFile.js and sketch.js. See the "Writing Tests" section below.
- tools folder: Contains a Python script for converting Playwright test output files to the Gradescope format.
- grading.config: Settings for the autograder. Ignore for now.
- run_autograder: The test runner script required by Gradescope. This script currently only handles submissions of a single sketch. This will likely be modified to handled submission of multiple sketches at the same time (e.g. for an entire practical at once).
- setup.sh: Required by Gradescope, this script installs all software required to run the tests (e.g. bash, Node).

# Writing tests
## Setup
Before you write any tests, you will need to get the staging folder ready to run Playwright tests. First, in the terminal, set the working directory to the staging folder e.g.

```cd staging```

(The command above assumes you are starting from the project folder)

Next, install all dependencies:
```npm install```

You should see a folder called node_modules appear in the staging folder.

## Add tests to staging/autograderTests/testFile.js
Write your tests in the runTests function already in testFile.js. Tests can take any format but each test should result in a pass or fail with a student-facing message, which is added to the TestResults object as shown in the comments in testFile.js. 

You will find lots of utility functions and some pre-defined tests for common functionality (e.g. checking the canvas is a specified size) in staging/testingDependencies/test-utils.js. These functions are toward the bottom of test-utils, in two regions: "GENERAL PURPOSE FUNCTIONS" and "GENERIC TESTS THAT MIGHT BE USEFUL".

## Test and run the tests
Before uploading the autograder to Gradescope, you should test your tests by running them on a selection of sample solutions e.g. a fully correct solution and solutions with each problem you are testing for. A sample solution is just a sketch file (sketch.js) that you put in the staging folder. It should be at the same level as index.html. You can run index.html using Live Preview to check the sketch visually.

Tests are run from the command line. Make sure your Terminal is running in the staging folder, then run:

```npx playwright test```

The first time Playwright is run, you will likely need to install more components. Follow the prompts in the Terminal.

Test output will be shown in the terminal. You can also see the full output in staging/ctrf/ctrf-report.json. The tests you defined in testFile.js are run as "steps" of a larger test (Test p5.js sketch > Run output tests). If even one of your tests fails, the larger test will also fail. 

# Create the autograder
- Zip the contents of this repo (just the contents, not the repo folder) and name it autograder.zip.
- In the VLE site (assuming you have Gradescope enabled for your site already), go to the Details & Actions menu (on the right) and click "View course & institution tools".
- Choose Gradescope. You may need to click "Browse all course tools" to find it.
- A wizard will appear asking you to link to an assignment. Choose "A new Gradescope assignment".
- On the next screen, choose "Programming assignment" from the "Assignment type" menu.
- Fill in the form fields as appropriate. Set the autograder points to the number of tests e.g. if you wrote 5 tests, there should be 5 points.
- The assignment will now appear as a VLE item. Click on it to go to the configuration screen.
- Click the "Select Autograder (.zip)" button and upload the zip file from the first step in this section. Click "Update Autograder". Gradescope will now try to build your autograder, which can take a minute or two.
- When you see "built as of ..." under the "Docker image status" heading, click the "Test Autograder" link next to the "Update Autograder" button. This will allow you to run the autograder on your sample solutions and see how the output appears to students.
- If you need to make changes to the autograder, recreate the zip file then return to the Gradescope assignment configuration screen and click the "Update Autograder" to replace the previous version.
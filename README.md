# Repo Contents

This autograder template was created using [this Jest autograder](https://github.com/ucsb-gradescope-tools/jest-autograder) as a reference.

Description of repo contents: 
- sampleSolutions folder: (Optional) Put your sample solutions (just the sketch.js files and assets folders, if required) here for use when testing your tests.
- staging folder: This is where the testing happens. Read the "Writing Tests" section below before editing / moving any files.
- tools folder: Contains a Python script for converting Playwright test output files to the Gradescope format.
- run_autograder: The test runner script required by Gradescope. This script should not be edited unless you are making major changes to the structure.
- setup.sh: Required by Gradescope, this script installs all software required to run the tests (e.g. bash, Node). This script should not be edited.

# Writing tests
## Setup
Before you write any tests, you will need to get the staging folder ready to run Playwright tests. First, in the terminal, set the working directory to the staging folder e.g.

```cd staging```

(The command above assumes you are starting from the project folder)

Next, install all dependencies:
```npm install```

You should see a folder called node_modules appear in the staging folder.

## Add tests to staging
Add test files for each sketch you are autograding into the sketches folder inside the staging folder. Each sketch to be autograded should be in its own folder in the sketches folder. For example, if submissions will contain two sketches, your staging folder might look something like:

```
staging
  |__sketches
       |__ sketch1
       |__ sketch2
```
 Each sketch to be autograded will need an index.html file in the staging folder. This file should link all necessary JS files. **Important:** The p5js folder and testingDependency folder will be copied into each sketch folder when the autograder runs so the file paths used to link each file should reflect this, as shown below. 

- The main p5js library: ```<script src="./p5js/p5.min.js"></script>``` . This tag should be placed in the ```<head></head>``` of index.html.
- The p5js sound library, if required: ```<script src="./p5js/p5.sound.min.js"></script>``` . This tag should be placed in the ```<head></head>``` of index.html.
- preload.js (in testingDependencies): ```<script src="./testingDependencies/preload.js"></script>```. This tag should be placed at the end of the ```<body></body>``` of index.html.
- sketch.js (the sketch code, must be called sketch.js). This is the file to be autograded and it will be automatically copied in when the autograder runs. Use ```<script src="sketch.js"></script>```. This tag should be placed at the end of the ```<body></body>``` of index.html, immediately after preload.js.
- test-utils.js (in testingDependencies): ```<script src="./testingDependencies/test-utils.js"></script>```. This tag should be placed at the end of the ```<body></body>``` of index.html, immediately after script.js.
- a .js test file. This should be linked at the end of the ```<body></body>``` of index.html, immediately after test-utils.js.

**See the existing template index.html files. You should be able to use the contents of an existing file and just update the name of the test file as needed.**

Write your tests in the test file for each sketch, following the format shown in the templates (e.g. sketches/sketch1/testFileSketch1.js). Tests can take any form but each test should result in a pass or fail with a student-facing message, which is then added to the TestResults object as shown in the comments in testFile.js. 

You will find lots of utility functions and some pre-defined tests for common functionality (e.g. checking the canvas is a specified size) in staging/testingDependencies/test-utils.js. These functions are toward the bottom of test-utils in two regions: "GENERAL PURPOSE FUNCTIONS" and "GENERIC TESTS THAT MIGHT BE USEFUL".

## Test and run your tests
Before uploading the autograder to Gradescope, you should test your tests by running them on a selection of sample solutions e.g. a fully correct solution and solutions with each potential problem you are testing for. 

To test your tests, copy the following dependencies from staging into each sketch folder (assumes you have followed the setup steps above):
- autograderTests
- node_modules
- p5js
- testingDependcies
- package-lock.json
- package.json
- playwright.config.js
- A sample solution sketch.js file and an assets folder if needed

Note: all of the above folders and files should be removed from the sketch folders once you are done testing your tests.

Tests are run from the command line. Make sure your Terminal is running in the sketch folder that you want to test, then run:

```npx playwright test```

The first time Playwright is run, you will likely need to install more components. Follow the prompts in the Terminal.

Test output will be shown in the terminal. You can also see the full output in ctrf/ctrf-report.json inside the sketch folder. The tests you defined in testFile.js are run as "steps" of a larger test (Test p5.js sketch > Run output tests). If even one of your tests fails, the larger test will also fail. Students will only see the step results.

# Create the autograder
- Zip the contents of this repo (just the contents, not the repo folder) and name it autograder.zip.
- In the VLE site (assuming you have Gradescope enabled already), go to the Details & Actions menu (on the right) and click "View course & institution tools".
- Choose Gradescope. You may need to click "Browse all course tools" to find it.
- A wizard will appear asking you to link to an assignment. Choose "A new Gradescope assignment".
- On the next screen, choose "Programming assignment" from the "Assignment type" menu.
- Fill in the form fields as appropriate. Set the autograder points to the number of tests e.g. if you wrote 5 tests, there should be 5 points.
- The assignment will now appear as a VLE item. Click on it to go to the configuration screen.
- Click the "Select Autograder (.zip)" button and upload the zip file from the first step in this section. Click "Update Autograder". Gradescope will now try to build your autograder, which can take a minute or two.
- When you see "built as of ..." under the "Docker image status" heading, click the "Test Autograder" link next to the "Update Autograder" button. This will allow you to run the autograder on your sample solutions and see how the output appears to students.
- If you need to make changes to the autograder, recreate the zip file then return to the Gradescope assignment configuration screen and click the "Update Autograder" to replace the previous version.
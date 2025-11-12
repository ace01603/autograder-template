'''
Run this script to test all available tests on all sample solutions.
The terminal should be at the root level of the repo when the script is run

This script depends on the following file structure:
- The staging > sketches folder must contain a folder for each exercise e.g. sketch1. Each exercise folder must 
  contain a properly prepared index.html (see the README) and a test file with the tests for the sketch.
- The sampleSolutions folder should contain a folder for each exercise. The names must match. E.g. if 
  staging > sketches contains a folder called sketch1, then sampleSolutions should contain a folder of the same
  name.
- Inside each sketch folder in the sampleSolutions folder, add folders for each potential solution (e.g. at 
  least one correct and at least one incorrect). Each of these folders should contain a sketch.js file with a 
  sample solution.
'''
import os
import shutil
import json

SAMPLE_SOLUTIONS = "sampleSolutions"
SKETCHES = "sketches"
STAGING = "staging"
AUTOGRADER_TESTS = "autograderTests"
NODE_MODULES = "node_modules"
P5JS = "p5js"
TESTING_DEPENDENCIES = "testingDependencies"
PACKAGE_LOCK = "package-lock.json"
PACKAGE = "package.json"
PLAYWRIGHT_CONFIG = "playwright.config.js"
SKETCH = "sketch.js"
CTRF = "ctrf"
TEST_RESULTS = "test-results"
SKETCH_TEST_RESULTS = "ctrf/ctrf-report.json"
LOCAL_TEST_RESULTS = "localTestResults.json"

all_test_results = []

def setup_sketch_folders(solution_folders):
    '''
    Copies the test dependencies into the sketch folder for testing
    '''
    for solution in solution_folders:
        print(solution)
        sketch_folder = STAGING + "/" + SKETCHES + "/" + solution
        if os.path.isdir(sketch_folder):
            shutil.copytree(STAGING + "/" + AUTOGRADER_TESTS, sketch_folder + "/" + AUTOGRADER_TESTS)
            shutil.copytree(STAGING + "/" + P5JS, sketch_folder + "/" + P5JS)
            shutil.copytree(STAGING + "/" + TESTING_DEPENDENCIES, sketch_folder + "/" + TESTING_DEPENDENCIES)
            shutil.copyfile(STAGING + "/" + PACKAGE_LOCK, sketch_folder + "/" + PACKAGE_LOCK)
            shutil.copyfile(STAGING + "/" + PACKAGE, sketch_folder + "/" + PACKAGE)
            shutil.copyfile(STAGING + "/" + PLAYWRIGHT_CONFIG, sketch_folder + "/" + PLAYWRIGHT_CONFIG)


def run_tests(sketch_name, sample):
    '''
    Runs the test on the current sample solution
    '''
    sample_solution_dir = SAMPLE_SOLUTIONS + "/" + sketch_name + "/" + sample
    if os.path.isdir(sample_solution_dir):
        shutil.copyfile(sample_solution_dir + "/" + SKETCH, STAGING + "/" + SKETCHES + "/" + sketch_name + "/" + SKETCH)
        # cd into sketch folder
        os.chdir(STAGING + "/" + SKETCHES + "/" + sketch_name)
        if not os.path.isdir(NODE_MODULES):
            os.system("npm install")
            os.system("npm install serve")
            os.system("npx playwright install --with-deps chromium")
        os.system("npx playwright test") # add --debug to debug tests
        # cd back to root
        os.chdir("../../../")
        # save the test results
        all_test_results.append(get_test_results(sketch_name, sample))


def get_test_results(sketch_name, current_solution):
    test_out = {
        "sketch": sketch_name,
        "version": current_solution,
        "test-results": []
    }
    test_results = STAGING + "/" + SKETCHES + "/" + sketch_name + "/" + SKETCH_TEST_RESULTS
    with open(test_results, "r") as json_file:
        raw_json = json.load(json_file)
        test_results = raw_json["results"]["tests"]
        for test in test_results:
            test_out["test-results"] += test["steps"]
    return test_out


def clean_up(solution_folders):
    '''
    Removes all files added to the staging area during testing
    '''
    for solution in solution_folders:
        sketch_folder = STAGING + "/" + SKETCHES + "/" + solution
        if os.path.isdir(sketch_folder):
            shutil.rmtree(sketch_folder + "/" + AUTOGRADER_TESTS)
            shutil.rmtree(sketch_folder + "/" + NODE_MODULES)
            shutil.rmtree(sketch_folder + "/" + P5JS)
            shutil.rmtree(sketch_folder + "/" + TESTING_DEPENDENCIES)
            os.remove(sketch_folder + "/" + PACKAGE_LOCK)
            os.remove(sketch_folder + "/" + PACKAGE)
            os.remove(sketch_folder + "/" + PLAYWRIGHT_CONFIG)
            os.remove(sketch_folder + "/" + SKETCH)
            shutil.rmtree(sketch_folder + "/" + CTRF)
            shutil.rmtree(sketch_folder  + "/" + TEST_RESULTS)


def filter_sketches(samples, to_test):
    if len(to_test) == 0:
        return samples
    filtered = []
    for s in samples:
        for t in to_test:
            if s.endswith(t):
                filtered.append(s)
                break
    return filtered


if __name__ == "__main__":
    # Choose a subset of sketches to test or leave empty to test them all
    selected_sketches = []# ["sketch1"]
    # delete previous test results
    if os.path.exists(SAMPLE_SOLUTIONS + "/" + LOCAL_TEST_RESULTS):
        os.remove(SAMPLE_SOLUTIONS + "/" + LOCAL_TEST_RESULTS)
    # list all folders in sampleSolutions
    sketches_with_sample_solutions = os.listdir(SAMPLE_SOLUTIONS)
    # filter if needed
    sketches_with_sample_solutions = filter_sketches(sketches_with_sample_solutions, selected_sketches)
    setup_sketch_folders(sketches_with_sample_solutions)
    for sketch in sketches_with_sample_solutions:
        if os.path.isdir(SAMPLE_SOLUTIONS + "/" + sketch):
            solutions_to_test = os.listdir(SAMPLE_SOLUTIONS + "/" + sketch)
            for sample in solutions_to_test:
                run_tests(sketch, sample)
    clean_up(sketches_with_sample_solutions)
    # write the test results
    with open(SAMPLE_SOLUTIONS + "/" + LOCAL_TEST_RESULTS, "w") as result_store:
        json.dump({ "results": all_test_results}, result_store, indent = 2, sort_keys = False)
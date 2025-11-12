#!/usr/bin/env python3
'''
This script is based on a Jest autograder for Gradescope
https://github.com/ucsb-gradescope-tools/jest-autograder/blob/main/tools/jest_to_gradescope.py
'''

import json
import argparse
import os
from pathlib import Path

def flatten_playwright_results(test_results):
    gradescope_results = []
    for test in test_results:
        visibiliy = "hidden"
        try:
            annotations = test["extra"]["annotations"]
            for a in annotations:
                if a["type"] == "visibility":
                    visibility = a["description"]
                    break
        except:
            print("Unable to find visibility of test results")
        if len(test["steps"]) > 0:
            for step in test["steps"]:
                step["score"] = 1.0 if step["status"] == "passed" else 0.0
                step["visibility"] = visibility
                gradescope_results.append(step)
        else:
            gradescope_results.append({
                "name": test["name"],
                "status": test["status"],
                "score": 1.0 if test["status"] == "passed" else 0.0,
                "visibility": visibility
            })
    return gradescope_results


def find_all_test_output():
    # Get the folder names in sketches
    sketches_dir = "sketches"
    output_file = "eslint.json"
    output_dir = "ctrf"
    output_bad_format = "bad-format.json"

    playwright_sketches = []
    eslint_sketches = []
    bad_format_sketches = []
    good_format_sketches = []

    dir_list = os.listdir(sketches_dir)
    # MODIFY THIS TO ALWAYS SHOW OUTPUT FORMAT TEST (output should be visible to students)
    for file in dir_list:
        if os.path.isdir(sketches_dir + "/" + file):
            sketch_files = os.listdir(sketches_dir + "/" + file)
            if output_bad_format in sketch_files:
                bad_format_sketches.append(file)
            else:
                good_format_sketches.append(file)
            if output_dir in sketch_files:
                playwright_sketches.append(file)
            if output_file in sketch_files:
                eslint_sketches.append(file)
    return playwright_sketches, eslint_sketches, bad_format_sketches, good_format_sketches
    

def process_playwright_output(sketches_with_playwright):
    gradescope_tests = []

    for sketch in sketches_with_playwright:
        playwright_output = "sketches/" + (sketch + "/" if sketch != "" else "") + "ctrf/ctrf-report.json"
        result_prefix = "" if sketch == "" else sketch + ": "
        with open(playwright_output, 'r') as json_data:
            raw_json = json.load(json_data)
            converted = flatten_playwright_results(raw_json["results"]["tests"])
            for result in converted:
                result["name"] = result_prefix + result["name"]
                # result["visibility"] = visibility
            gradescope_tests += converted
    
    return gradescope_tests


def process_eslint_output(sketches_with_eslint):
    eslint_tests = []

    for sketch in sketches_with_eslint:
        eslint_output = "sketches/" + (sketch + "/" if sketch != "" else "") + "eslint.json"
        result_prefix = "Code style: " if sketch == "" else sketch + " code style: "
        with open(eslint_output, "r") as json_data:
            try:
                raw_json = json.load(json_data)
                # name, status, score
                for file in raw_json:
                    for msg in file["messages"]:
                        eslint_tests.append({
                            "name": f'{result_prefix}{msg["message"]} Line {msg["line"]}. Column {msg["column"]}. Rule ID: {msg["ruleId"]}.',
                            "status": "failed",
                            "score": 0.0
                        })
            except:
                print("Unable to decode JSON from", sketch, "eslint test")

    return eslint_tests


def process_bad_format(sketches_with_bad_format):
    bad_format_tests = []

    for sketch in sketches_with_bad_format:
        json_file = "sketches/" + sketch + "/bad-format.json"
        with open(json_file) as json_data:
            bad_format_tests += json.load(json_data)
    return bad_format_tests


def process_good_format(sketches_with_good_format):
    good_format_tests = []
    for sketch in sketches_with_good_format:
        good_format_tests.append({
                            "name": f'Found sketch.js file for {sketch}.',
                            "status": "passed",
                            "score": 0.0,
                            "visibility": "visible"
        })
    return good_format_tests


def main():
    # Initialize command line arguments
    parser = argparse.ArgumentParser()

    parser.add_argument("-o", "--output", help="Output file to produce (in Gradescope format)")
    args = parser.parse_args()

    # Search for all ctrf files
    sketches_with_playwright, sketches_with_eslint, sketches_with_bad_format, sketches_with_good_format = find_all_test_output()
    
    gradescope_tests = process_bad_format(sketches_with_bad_format)
    gradescope_tests += process_good_format(sketches_with_good_format)
    gradescope_tests += process_playwright_output(sketches_with_playwright)
    gradescope_tests += process_eslint_output(sketches_with_eslint)


    print("gradescope_tests",json.dumps({ "tests": gradescope_tests}, indent=2))

    if args.output != None:
      with open(args.output,'w') as json_data:
        json.dump({ "tests": gradescope_tests}, json_data,indent=2,sort_keys=True)


if __name__=="__main__":
    main()


'''
{
  "tests": [
    {
      "name": "1.1-Shapes1: Your canvas is the expected size.",
      "status": "passed",
      "score": 1.0
    },
    {
      "name": "1.1-Shapes1: 3 shapes were drawn, as expected.",
      "status": "passed",
      "score": 1.0
    },
    {
      "name": "1.1-Shapes1: Sketch includes a 75 x 30 ellipse at 50, 100.",
      "status": "passed",
      "score": 1.0
    },
    {
      "name": "1.1-Shapes1: Could not find a 100 pixel square at 300, 80.",
      "status": "failed",
      "score": 0.0
    },
    {
      "name": "1.1-Shapes1: Sketch includes a triangle with corners at 200, 250; 400, 450; 125, 500.",
      "status": "passed",
      "score": 1.0
    }
  ]
}
'''
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
        if len(test["steps"]) > 0:
            for step in test["steps"]:
                step["score"] = 1.0 if step["status"] == "passed" else 0.0
                gradescope_results.append(step)
        else:
            gradescope_results.append({
                "name": test["name"],
                "status": test["status"],
                "score": 1.0 if test["status"] == "passed" else 0.0
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

    dir_list = os.listdir(sketches_dir)

    for file in dir_list:
        if os.path.isdir(sketches_dir + "/" + file):
            sketch_files = os.listdir(sketches_dir + "/" + file)
            if output_bad_format in sketch_files:
                bad_format_sketches.append(file)
            if output_dir in sketch_files:
                playwright_sketches.append(file)
            if output_file in sketch_files:
                eslint_sketches.append(file)
    return playwright_sketches, eslint_sketches, bad_format_sketches
    

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


def main():
    # Initialize command line arguments
    parser = argparse.ArgumentParser()

    parser.add_argument("-o", "--output", help="Output file to produce (in Gradescope format)")
    args = parser.parse_args()

    # Search for all ctrf files
    sketches_with_playwright, sketches_with_eslint, sketches_with_bad_format = find_all_test_output()
    
    gradescope_tests = process_bad_format(sketches_with_bad_format)
    gradescope_tests += process_playwright_output(sketches_with_playwright)
    gradescope_tests += process_eslint_output(sketches_with_eslint)


    print("gradescope_tests",json.dumps(gradescope_tests, indent=2))

    if args.output != None:
      with open(args.output,'w') as json_data:
        json.dump({ "tests": gradescope_tests}, json_data,indent=2,sort_keys=True)


if __name__=="__main__":
    main()
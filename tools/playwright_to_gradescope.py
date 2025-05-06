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


def find_all_playwright_output():
    # Get the folder names in sketches
    sketches_dir = "sketches"
    output_dir = "ctrf"
    dir_list = os.listdir(sketches_dir)
    if output_dir in dir_list:
        # no sketch folders, output at top level
        print("Sketch at top level")
        return [""]
    else:
        sketches = []
        for file in dir_list:
            if os.path.isdir(sketches_dir + "/" + file):
                if output_dir in os.listdir(sketches_dir + "/" + file):
                    print(file + "is a sketch with output")
                    sketches.append(file)
        return sketches
    


def main():
    # Initialize command line arguments
    parser = argparse.ArgumentParser()

    parser.add_argument("-o", "--output", help="Output file to produce (in Gradescope format)")
    args = parser.parse_args()

    # Search for all ctrf files
    sketches = find_all_playwright_output()
    gradescope_tests = []

    for sketch in sketches:
        playwright_output = "sketches/" + (sketch + "/" if sketch != "" else "") + "ctrf/ctrf-report.json"
        result_prefix = "" if sketch == "" else sketch + ": "
        with open(playwright_output, 'r') as json_data:
            raw_json = json.load(json_data)
            converted = flatten_playwright_results(raw_json["results"]["tests"])
            for result in converted:
                result["name"] = result_prefix + result["name"]
            gradescope_tests += converted



    print("gradescope_tests",json.dumps(gradescope_tests, indent=2))

    if args.output != None:
      with open(args.output,'w') as json_data:
        json.dump({ "tests": gradescope_tests}, json_data,indent=2,sort_keys=True)


if __name__=="__main__":
    main()
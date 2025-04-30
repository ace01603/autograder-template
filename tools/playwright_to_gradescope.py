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


def main():

    # Initialize command line arguments
    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--input", help="Input file to read (produced by Playwright)")
    parser.add_argument("-o", "--output", help="Output file to produce (in Gradescope format)")
    args = parser.parse_args()


    playwright_data = {}

    if args.input != None:
        with open(args.input,'r') as json_data:
            playwright_data = json.load(json_data)
    
    # assertions = playwright_data["results"]["tests"] # list(flatten(map(lambda x:x["assertionResults"], playwright_data["testResults"])))
    
    gradescope_tests = flatten_playwright_results(playwright_data["results"]["tests"]) # list(map(playwright_assertion_to_gradescope, assertions))

    # if not playwright_data["success"]:
    #     messages = "\n".join(list(map(lambda x:x["message"].replace("\"","\\\""), playwright_data["testResults"])))
        
    #     gradescope_tests.append({
    #             "name": "jest test failed",
    #             "max_score": 1,
    #             "score": 0, 
    #             "output": messages
    #     })

    # print("jest_data",json.dumps(playwright_data, indent=2))
    # print("asssertions",json.dumps(assertions, indent=2))
    print("gradescope_tests",json.dumps(gradescope_tests, indent=2))

    if args.output != None:
      with open(args.output,'w') as json_data:
        json.dump({ "tests": gradescope_tests}, json_data,indent=2,sort_keys=True)


if __name__=="__main__":
    main()
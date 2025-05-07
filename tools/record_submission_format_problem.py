import json
import argparse
import os
from pathlib import Path

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--sketch", help="Name of sketch folder that is missing or incorrectly formatted")
    args = parser.parse_args()

    with open("/autograder/source/staging/sketches/" + args.sketch + "/bad-format.json", "w") as json_data:
        json.dump([
            {
                "name": f"Unable to find your code for {args.sketch}. Your submission must contain a folder called {args.sketch} which must contain your code in a file called sketch.js.",
                "status": "failed",
                "score": 0.0
            }
        ], json_data, indent=2, sort_keys=True)
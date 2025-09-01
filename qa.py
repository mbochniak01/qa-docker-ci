#!/usr/bin/env python3
"""
QA CLI wrapper for Makefile commands
Usage:
    python qa.py [all|build|test|report|clean|ci]
"""

import subprocess
import sys

VALID_TARGETS = ["all", "build", "test", "report", "clean", "ci"]

def run_make(target: str):
    print(f"Running QA target: {target}")
    try:
        subprocess.run(["make", target], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: make {target} failed with exit code {e.returncode}")
        sys.exit(e.returncode)

def main():
    target = sys.argv[1] if len(sys.argv) > 1 else "all"
    if target not in VALID_TARGETS:
        print(f"Unknown target: {target}")
        print(f"Usage: python {sys.argv[0]} [{'|'.join(VALID_TARGETS)}]")
        sys.exit(1)
    run_make(target)

if __name__ == "__main__":
    main()

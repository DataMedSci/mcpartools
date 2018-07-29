#!/usr/bin/env bash

# Exit immediately if a simple command exits with a non-zero status.
set -e

INPUT_WILDCARD={output_dir:s}/workspace/job_*/{wildcard:s}
OUTPUT_DIRECTORY={output_dir:s}/output

# change working directory
cd {output_dir:s}

# make output folder
mkdir -p $OUTPUT_DIRECTORY

{collect_action:s}
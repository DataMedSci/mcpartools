#!/usr/bin/env bash

# Exit immediately if a simple command exits with a non-zero status.
set -e

INPUT_WILDCARD={output_dir:s}/workspace/job_*/*.bdo
OUTPUT_DIRECTORY={output_dir:s}/output

# make output folder
mkdir -p $OUTPUT_DIRECTORY

{collect_action:s}
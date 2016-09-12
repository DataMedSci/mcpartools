#!/usr/bin/env bash

# Exit immediately if a simple command exits with a non-zero status.
set -e

# make output folder
mkdir -p {output_dir:s}/output

# copy all binary output files to the same folder
for f in {output_dir:s}/workspace/job_*/*.bdo; do
  cp $f {output_dir:s}/output/
done
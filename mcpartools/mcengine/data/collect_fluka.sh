#!/usr/bin/env bash
# make output folder
mkdir -p {output_dir:s}/output
# copy all output files to the same folder
for f in {output_dir:s}/workspace/job_*/*_fort.*; do
  cp $f {output_dir:s}/output/;
done

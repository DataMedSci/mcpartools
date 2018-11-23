#!/usr/bin/env bash

# Exit immediately if a simple command exits with a non-zero status.
set -e

# location of FLUKA binary file
FLUKA_BIN={fluka_bin:s}

# go to working directory
cd {working_directory:s}

# run rfluka
$FLUKA_BIN -N0 -M1 {engine_options:s} {input_basename:s}

# each fluka run will save files with same name, in order to distinguish output from multiple runs
# we rename output files, appending suffix with jobid to each of them
# this will facilitate later data merging
for f in {input_basename:s}001*; do mv $f {input_basename:s}{job_id:04d}${{f#{input_basename:s}001}}; done
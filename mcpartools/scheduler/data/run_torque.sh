#!/usr/bin/env bash

set -e # Exit immediately if a simple command exits with a non-zero status.

# Run individual jobs
{workspace_dir:s}/job_`for((i=1;i<={jobs_no:d};i+=1)); do printf %04d; done`/run.sh

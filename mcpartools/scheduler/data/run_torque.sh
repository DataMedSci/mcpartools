#!/usr/bin/env bash

set -e # Exit immediately if a simple command exits with a non-zero status.

# Run individual jobs
{workspace_dir:s}/job_`printf %04d $SLURM_ARRAY_TASK_ID`/run.sh

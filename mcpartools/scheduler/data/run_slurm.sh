#!/usr/bin/env bash
# Exit immediately if a simple command exits with a non-zero status.
set -e

{options_header:s}

# Run individual jobs
{workspace_dir:s}/job_`printf %04d $SLURM_ARRAY_TASK_ID`/run.sh

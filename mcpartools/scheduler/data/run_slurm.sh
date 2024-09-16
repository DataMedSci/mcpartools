#!/usr/bin/env bash
# Exit immediately if a simple command exits with a non-zero status.
set -e
{trap_sig:s}
{options_header:s}

# Run individual jobs
source {workspace_dir:s}/job_`printf %04d $SLURM_ARRAY_TASK_ID`/run.sh

{check_running:s}
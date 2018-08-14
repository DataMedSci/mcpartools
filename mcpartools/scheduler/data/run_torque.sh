#!/usr/bin/env bash
#PBS -l select=1:ncpus=3:mem=1gb
#PBS -A ccbmc7
# Exit immediately if a simple command exits with a non-zero status.
set -e

{options_header:s}

# Run individual jobs
{workspace_dir:s}/job_`printf %04d $PBS_ARRAY_INDEX`/run.sh

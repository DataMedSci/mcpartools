#!/bin/bash

LOGFILE="$(dirname $0)/submit.log"
printf "Job ID: " > "$LOGFILE"

sbatch {options_args:s} --array=1-{jobs_no:d} --output="{log_dir:s}/output_%j_%a.log" --error="{log_dir:s}/error_%j_%a.log" --parsable {script_path:s} | cut -d ";" -f 1 >> "$LOGFILE"

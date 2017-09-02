#!/bin/bash

# Log file submit.log will be created in the same directory submit.sh is located
LOGFILE="$(cd $(dirname $0) && pwd)/submit.log"
printf "Job ID: " > "$LOGFILE"

sbatch {options_args:s} --array=1-{jobs_no:d} --output="{log_dir:s}/output_%j_%a.log" --error="{log_dir:s}/error_%j_%a.log" --parsable {script_path:s} | cut -d ";" -f 1 >> "$LOGFILE" && echo "Saving logs to $LOGFILE"

#!/usr/bin/env bash

# Log file submit.log will be created in the same directory submit.sh is located
LOGFILE="$(cd $(dirname $0) && pwd)/submit.log"
echo "Saving logs to $LOGFILE"
printf "Job ID: " > "$LOGFILE"

qsub {options_args:s} -t 1-{jobs_no:d} -o {log_dir:s} -e {log_dir:s} -terse {script_path:s} >> "$LOGFILE"

printf "Submission time: `date +"%Y-%m-%d %H:%M:%S"`" >> "$LOGFILE

#!/usr/bin/env bash

LOGFILE="$(dirname $0)/submit.log"
printf "Job ID: " > "$LOGFILE"

qsub {options_args:s} -t 1-{jobs_no:d} -o {log_dir:s} -e {log_dir:s} -terse {script_path:s} >> "$LOGFILE"

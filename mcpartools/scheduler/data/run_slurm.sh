#!/usr/bin/env bash
# Exit immediately if a simple command exits with a non-zero status.
set -e

{options_header:s}

_term() {{
  echo Caught SIGUSR1 signal in main run script, resending!
  kill -SIGUSR1 $PID 2>/dev/null
}}

trap _term SIGUSR1

# Run individual jobs
source {workspace_dir:s}/job_`printf %04d $SLURM_ARRAY_TASK_ID`/run.sh

# Check is executable still running
IS_RUNNING=`eval ps -p $PID | wc -l`
while [[ $IS_RUNNING -eq 2 ]]; do
   IS_RUNNING=`eval ps -p $PID | wc -l`
   sleep 0.5
done
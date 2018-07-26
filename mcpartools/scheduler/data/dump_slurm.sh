#!/bin/bash

# Exit immediately if a simple command exits with a non-zero status.
set -e

MIN_NUM=1
JOB_NUM={jobs_no:d}
RUN_DIR={main_dir:s}
DUMP_DIR="{main_dir:s}/dumped/`date '+%Y%m%d_%H%M%S'`/"
COLLECT=0
COLLECT_BIN="{main_dir:s}/{collect_script_name:s} -d $DUMP_DIR"
WORKSPACE_DIR={workspace_dir:s}

function usage () {{
   cat <<EOF
Usage: $progname [-c] [-m <num>]
where:
    -m set minimal number of correctly dumped jobs
       from which you can collect the results (1 by default)
    -c collect after dump
EOF
   exit 0
}}

while getopts ":cm:" opt; do
  case $opt in
    m)
      if ! [[ $OPTARG =~ '^[0-9]+$' ]] ; then
         echo "error: \"$OPTARG\" is not a number" >&2; exit 1
      elif [[ "$OPTARG" -gt "$JOB_NUM"  ]] ; then
 	 echo "error: $OPTARG is bigger then number of jobs ($JOB_NUM)" >&2; exit 1
      fi
      echo "-m was triggered, Parameter: $OPTARG" >&2
      MIN_NUM=$OPTARG
      ;;
    c)
      COLLECT=1
      ;;
    \?)
      echo "Invalid option: -$OPTARG" >&2
      usage
      exit 1
      ;;
    :)
      echo "Option -$OPTARG requires an argument." >&2
      usage
      exit 1
      ;;
    *)
      usage
      exit 1
      ;;
  esac
done

{dump_function:s}

SIG_SENDER='scancel -b -s'
SIGNAL='{dump_signal:s}'
PID=''


eval "$SIG_SENDER $SIGNAL $PID"
mkdir -p $DUMP_DIR
dump_function
echo "Results dumped to $DUMP_DIR"
if [[ $COLLECT -eq 1 ]]; then
   echo "Collecting..."
   $COLLECT_BIN
fi


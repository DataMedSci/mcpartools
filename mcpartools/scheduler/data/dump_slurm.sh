#!/bin/bash

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
    -c collect after dump
EOF
   exit 0
}}

while getopts ":c" opt; do
  case $opt in
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

if [[ ! -z "$PID" ]] ; then
    eval "$SIG_SENDER $SIGNAL $PID" 2>/dev/null
    if [[ $? -ne 0 ]] ; then
        echo "Nothing to dump from. All jobs finished"
        exit 1
    fi
    mkdir -p $DUMP_DIR
    dump_function
    if [[ $COLLECT -eq 1 ]]; then
       echo "Collecting..."
       $COLLECT_BIN
    fi
    echo "Results dumped to $DUMP_DIR"
else
    echo "First run submit.sh and then try to dump results"
fi


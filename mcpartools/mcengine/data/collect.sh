#!/usr/bin/env bash

# Exit immediately if a simple command exits with a non-zero status.
set -e

function usage () {{
   cat <<EOF
Usage: $progname [-d <dir_name>]
where:
    -d collect on results from directory <dir_name>
EOF
   exit 0
}}

INPUT_WILDCARD={output_dir:s}/workspace/job_*/{wildcard:s}
OUTPUT_DIRECTORY={output_dir:s}/output

while getopts "d:" opt; do
  case $opt in
    d)
      INPUT_WILDCARD="$OPTARG/job_*/*.bdo"
      OUTPUT_DIRECTORY="$OPTARG/output"
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

# make output folder
mkdir -p $OUTPUT_DIRECTORY

{collect_action:s}
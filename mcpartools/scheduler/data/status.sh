#!/usr/bin/env bash

STATUS_CMD="{merge_script_path:s}"
SAVE_TO_FILE_FLAG=false
while getopts ":s" opt; do
  case $opt in
    s)
        SAVE_TO_FILE_FLAG=true
        STATUS_CMD="$STATUS_CMD -s"
        ;;
    h)
   cat <<EOF
        Usage: status [-s] [-h]
        where:
            -s create status file
            -h give this help list
EOF
        exit 0
        ;;
    \?)
      echo "Invalid option: -$OPTARG" >&2
      exit 1
      ;;
  esac
done

eval $STATUS_CMD
CMD_STATUS=$?

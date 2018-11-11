#!/usr/bin/env bash

FILE_NAME=status_`date +%Y%m%d_%H%M%S`.log

STATUS_CMD="{merge_script_path:s} workspace/$FILE_NAME"

eval $STATUS_CMD
CMD_STATUS=$?

if [[ $CMD_STATUS -eq 0 ]]
then
    echo "Status successfully saved to file: workspace/$FILE_NAME"
else
    echo "Unable to create status file"
fi
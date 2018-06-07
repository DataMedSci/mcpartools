#!/bin/bash

# submit.log is for storing stdout and stderr of submit.sh
LOGFILE="$(cd $(dirname $0) && pwd)/submit.log"

RE="Job ID: ([0-9]*)"

# no log file. Probably submit.sh not run
if [ ! -f $LOGFILE ]; then
    echo "File not found: $LOGFILE"
    echo "Make sure you run submit script"
    exit 1
fi

if [[ $(cat $LOGFILE) =~ $RE ]];
then
    JOB_ID=${BASH_REMATCH[1]};
fi

# if job id is empty probably submit script was not run properly
if [ -n "$JOB_ID" ]
then
    scancel ${JOB_ID}
    if [ $? -eq 0 ]; then
    echo "Jobs with id: $JOB_ID canceled successfully"
    else
        echo "Unable to cancel jobs"
    fi
else
    echo "Cannot extract job id from $LOGFILE"
    echo "Make sure submit was run without errors, check log file"
    exit 2
fi

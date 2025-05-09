#!/bin/bash

# submit.log is for storing stdout and stderr of submit.sh
LOGFILE="$(cd $(dirname $0) && pwd)/submit.log"

RE="Job ID: ([0-9]*\[\])"

# no log file. Probably submit.sh not run
if [ ! -f $LOGFILE ]; then
    echo "File not found: $LOGFILE"
    echo "Make sure you run submit script"
    exit 1
fi

cat ${LOGFILE} | while read line
do
    if [[ ${line} =~ $RE ]];
    then
        JOB_ID=${BASH_REMATCH[1]};
        if [ -n "$JOB_ID" ]
        then
            qdel ${JOB_ID}
            if [ $? -eq 0 ]; then
                echo "Job with id: $JOB_ID canceled successfully"
            else
                echo "Unable to cancel job: $JOB_ID"
            fi
        fi
    fi
done

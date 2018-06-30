#!/usr/bin/env bash

# Log file submit.log will be created in the same directory submit.sh is located
# submit.log is for storing stdout and stderr of qsub command, for log info from individual jobs see {log_dir:s} directory
LOGFILE="$(cd $(dirname $0) && pwd)/submit.log"
echo -n "" > "$LOGFILE"

# Create temporary files for parsing stdout and stderr output from qsub command before storing them in submit.log
OUT=`mktemp`
ERR=`mktemp`
# On exit or if the script is interrupted (i.e. by receiving SIGINT signal) delete temporary files
trap "rm -f $OUT $ERR" EXIT

qsub {options_args:s} -t 1-{jobs_no:d} -o {log_dir:s} -e {log_dir:s} -terse {script_dir:s}/{calculate_script_name:s} > $OUT 2> $ERR

echo "Saving logs to $LOGFILE"

# If qsub command ended with a success log following info
if [ $? -eq 0 ] ; then
        echo "Job ID: `cat $OUT | cut -d ";" -f 1`" > "$LOGFILE"
        echo "Submission time: `date +"%Y-%m-%d %H:%M:%S"`" >> "$LOGFILE"
fi

# If output from stderr isn't an empty string then log it as well to submit.log
if [ "`cat $ERR`" != "" ] ; then
        echo "---------------------" >> "$LOGFILE"
        echo "ERROR MESSAGE" >>"$LOGFILE"
        echo "---------------------" >> "$LOGFILE"
        cat $ERR >> "$LOGFILE"
fi

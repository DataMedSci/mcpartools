#!/usr/bin/env bash

# Log file submit.log will be created in the same directory submit.sh is located
# submit.log is for storing stdout and stderr of qsub command, for log info from individual jobs see {log_dir:s} directory
LOGFILE="$(cd $(dirname $0) && pwd)/submit.log"
echo -n "" > "$LOGFILE"

OUT=`mktemp`
ERR=`mktemp`
qsub {options_args:s} -t 1-{jobs_no:d} -o {log_dir:s} -e {log_dir:s} -terse {script_path:s} > $OUT 2> $ERR

echo "Saving logs to $LOGFILE"

# if qsub command ended with a success log following info
if [ $? -eq 0 ] ; then
        echo "Job ID: `cat $OUT | cut -d ";" -f 1`" > "$LOGFILE"
        echo "Submission time: `date +"%Y-%m-%d %H:%M:%S"`" >> "$LOGFILE"
fi

# if output from stderr isn't an empty string then log it as well to submit.log
if [ "`cat $ERR`" != "" ] ; then
        echo "---------------------" >> "$LOGFILE"
        echo "ERROR MESSAGE" >>"$LOGFILE"
        echo "---------------------" >> "$LOGFILE"
        cat $ERR >> "$LOGFILE"
fi

rm $OUT
rm $ERR

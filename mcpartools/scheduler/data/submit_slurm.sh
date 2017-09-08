#!/bin/bash

# Log file submit.log will be created in the same directory submit.sh is located
# submit.log is for storing stdout and stderr of sbatch command, for log info from individual jobs see {log_dir:s} directory
LOGFILE="$(cd $(dirname $0) && pwd)/submit.log"
echo -n "" > "$LOGFILE"

# Create temporary files for parsing stdout and stderr output from sbatch command before storing them in submit.log
OUT=`mktemp`
ERR=`mktemp`
# On exit or if the script is interrupted (i.e. by receiving SIGINT signal) delete temporary files
trap "rm -f $OUT $ERR" EXIT

sbatch {options_args:s} --array=1-{jobs_no:d} --output="{log_dir:s}/output_%j_%a.log" --error="{log_dir:s}/error_%j_%a.log" --parsable {script_path:s} > $OUT 2> $ERR

echo "Saving logs to $LOGFILE"

# If sbatch command ended with a success log following info
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

#!/bin/bash

# Log file submit.log will be created in the same directory submit.sh is located
# submit.log is for storing stdout and stderr of sbatch command, for log info from individual jobs see {log_dir:s} directory
LOGFILE="$(cd $(dirname $0) && pwd)/submit.log"
echo -n "" > "$LOGFILE"

OUT=`mktemp`
ERR=`mktemp`
sbatch {options_args:s} --array=1-{jobs_no:d} --output="{log_dir:s}/output_%j_%a.log" --error="{log_dir:s}/error_%j_%a.log" --parsable {script_path:s} > $OUT 2>$ERR

echo "Saving logs to $LOGFILE"

# if sbatch command ended with a success log following info
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

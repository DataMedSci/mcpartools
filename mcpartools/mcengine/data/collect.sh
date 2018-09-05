#!/usr/bin/env bash

# Exit immediately if a simple command exits with a non-zero status.
set -e

START=$(date +%s)

INPUT_WILDCARD={output_dir:s}/workspace/job_*/{wildcard:s}
OUTPUT_DIRECTORY={output_dir:s}/output
LOG_FILE=$OUTPUT_DIRECTORY/info.log

# change working directory
cd {output_dir:s}

# make output folder
mkdir -p $OUTPUT_DIRECTORY

echo "###########################################################" > $LOG_FILE
echo "################### COLLECT INFORMATION ###################" >> $LOG_FILE
echo "###########################################################" >> $LOG_FILE
echo "#" >> $LOG_FILE
echo "# START           = `date +"%Y-%m-%d %H:%M:%S"`" >> $LOG_FILE
echo "# END             =                   -" >> $LOG_FILE
echo "# TIME IN SECONDS =                   -" >> $LOG_FILE
echo "# STATUS          =                   1" >> $LOG_FILE
echo "#" >> $LOG_FILE

{collect_action:s}
COLLECT_STATUS=$?

let "EXECUTION_TIME = $(date +%s) - $START"

#    end time is in line number 6
sed -i "6s/.*/# END             = `date +"%Y-%m-%d %H:%M:%S"`/" $LOG_FILE
#    collapsed time is in line number 7
sed -i "7s/.*/# TIME IN SECONDS =`printf "%20d" $EXECUTION_TIME`/" $LOG_FILE
#    status is in line number 8
sed -i "8s/.*/# STATUS          =                   0/" $LOG_FILE

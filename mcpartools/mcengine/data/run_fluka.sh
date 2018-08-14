#!/usr/bin/env bash

# Exit immediately if a simple command exits with a non-zero status.
set -e

START=$(date +%s)

# location of FLUKA binary file
FLUKA_BIN={fluka_bin:s}

WORK_DIR={working_directory:s}
# go to working directory
cd $WORK_DIR

LOG_FILE=$WORK_DIR"/info.log"

echo "###########################################################" > $LOG_FILE
echo "######### DETAILED INFORMATION ABOUT JOB `printf "%5d" $RNG_SEED` ############" >> $LOG_FILE
echo "###########################################################" >> $LOG_FILE
echo "#" >> $LOG_FILE
echo "# START           = `date +"%Y-%m-%d %H:%M:%S"`" >> $LOG_FILE
echo "# END             =                   -" >> $LOG_FILE
echo "# TIME IN SECONDS =                   -" >> $LOG_FILE
echo "# NO OF PARTICLES =`printf "%20d" $PARTICLE_NO`" >> $LOG_FILE
echo "# STATUS          =                   -" >> $LOG_FILE
echo "#" >> $LOG_FILE

# run rfluka
$FLUKA_BIN -N0 -M1 {engine_options:s} {input_basename:s}
SIMULATION_STATUS=$?

let "EXECUTION_TIME = $(date +%s) - $START"

#    end time is in line number 6
sed -i "6s/.*/# END             = `date +"%Y-%m-%d %H:%M:%S"`/" $LOG_FILE
#    collapsed time is in line number 7
sed -i "7s/.*/# TIME IN SECONDS =`printf "%20d" $EXECUTION_TIME`/" $LOG_FILE
#    status is in line number 9
sed -i "9s/.*/# STATUS          =`printf "%20d" $SIMULATION_STATUS`/" $LOG_FILE

# each fluka run will save files with same name, in order to distinguish output from multiple runs
# we rename output files, appending suffix with jobid to each of them
# this will facilitate later data merging
for f in {input_basename:s}001*; do mv $f {input_basename:s}{job_id:04d}${{f#{input_basename:s}001}}; done
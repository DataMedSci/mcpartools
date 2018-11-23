#!/usr/bin/env bash

function initLogFile(){{
    START=$(date +%s)
    echo "###########################################################" > $LOG_FILE
    echo "######### DETAILED INFORMATION ABOUT JOB `printf "%5d" $SLURM_ARRAY_TASK_ID` ############" >> $LOG_FILE
    echo "###########################################################" >> $LOG_FILE
    echo "#" >> $LOG_FILE
    echo "# START           = `date +"%Y-%m-%dT%H:%M:%S"`" >> $LOG_FILE
    echo "# END             =                   -" >> $LOG_FILE
    echo "# TIME IN SECONDS =                   -" >> $LOG_FILE
    echo "# NO OF PARTICLES =`printf "%20d" $PARTICLES_NO`" >> $LOG_FILE
    echo "# STATUS          =                   -" >> $LOG_FILE
    echo "#" >> $LOG_FILE
}}

function completeLogFile(){{
    let "EXECUTION_TIME = $(date +%s) - $START"

    #    end time is in line number 6
    sed -i "6s/.*/# END             = `date +"%Y-%m-%dT%H:%M:%S"`/" $LOG_FILE
    #    collapsed time is in line number 7
    sed -i "7s/.*/# TIME IN SECONDS =`printf "%20d" $EXECUTION_TIME`/" $LOG_FILE
    #    status is in line number 9
    sed -i "9s/.*/# STATUS          =`printf "%20s" $SIMULATION_STATUS`/" $LOG_FILE
}}


{options_header:s}

WORKSPACE_PATH={workspace_dir:s}
JOB_DIR_PATH=$WORKSPACE_PATH/job_`printf %04d $SLURM_ARRAY_TASK_ID`

LOG_FILE=$JOB_DIR_PATH"/info.log"

PARTICLES_NO={particle_no:d}

initLogFile

# Run individual jobs
$JOB_DIR_PATH/run.sh

if [[ $? -ne 0 ]]
then
    SIMULATION_STATUS="ST"
else
    SIMULATION_STATUS="CD"
fi

completeLogFile
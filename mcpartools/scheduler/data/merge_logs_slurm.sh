#!/usr/bin/env bash

function writeLogHeader(){{
    echo "###########################################################" >> ${{LOG_FILE}}
    echo "############ START AND END OF JOBS EXECUTION ##############" >> ${{LOG_FILE}}
    echo "###########################################################" >> ${{LOG_FILE}}
    echo "#" >> ${{LOG_FILE}}
    echo "#    ID                START                  END     STATUS   TIME" >> ${{LOG_FILE}}
    echo "    ID                START                  END     STATUS   TIME"

    for i in ${{WORKSPACE}}/job_*;
    do
        JOB_DIR_NAME=$(basename $i)
        if [[ $JOB_DIR_NAME =~ $JOB_ID_REGEX ]];
        then
            JOB_ID=${{BASH_REMATCH[1]}};

            # remove 0 at the beginning of the number
            JOB_ID=$(expr $JOB_ID + 0)
        else
            echo "Cannot get job ID from $i file"
            continue
        fi

        JOB_STAT=`squeue -j${{ARRAY_JOB_ID}}_${{JOB_ID}} -o '%V %t %M' -h 2> /dev/null`
        SQUEUE_STATUS=$?

        if [[ $SQUEUE_STATUS -ne 0 || -z $JOB_STAT ]]
        then
            INFO_FILE=$i/$JOBS_LOG_FILE

            if [[ $(cat $INFO_FILE) =~ $START_REGEX ]];
            then
                START_TIME=${{BASH_REMATCH[1]}};
            else
                echo "Cannot get start time from $INFO_FILE file"
                continue
            fi

            if [[ $(cat $INFO_FILE) =~ $END_REGEX ]];
            then
                END_TIME=${{BASH_REMATCH[1]}};
            else
                echo "Cannot get end time from $INFO_FILE file"
                continue
            fi

            if [[ $(cat $INFO_FILE) =~ $STATUS_REGEX ]];
            then
                STATUS=${{BASH_REMATCH[1]}};
            else
                echo "Cannot get status from $i file"
                continue
            fi

            if [[ $(cat $INFO_FILE) =~ $COLLAPSED_TIME_REGEX ]];
            then
                COLLAPSED_TIME=${{BASH_REMATCH[1]}};
            else
                echo "Cannot get collapsed time from $i file"
                continue
            fi

        else
            START_TIME=`echo ${{JOB_STAT}} | cut -d ' ' -f 1`
            STATUS=`echo ${{JOB_STAT}} | cut -d ' ' -f 2`
            COLLAPSED_TIME=`echo ${{JOB_STAT}} | cut -d ' ' -f 3`
            if [[ -z $COLLAPSED_TIME ]]
            then
                COLLAPSED_TIME='0'
            else
                COLLAPSED_TIME=`echo $COLLAPSED_TIME | awk -F ":" '{{ print $1 * 60 + $2 }}'`
            fi

            END_TIME="-"
        fi

        TASK_NUMBER=$((TASK_NUMBER + 1))


        if [[ ${{STATUS}} == "CD" ]]
        then
            SUCCESSES=$((SUCCESSES + 1))
            TOTAL_TIME=$((TOTAL_TIME + $COLLAPSED_TIME))
        elif [[ ${{STATUS}} != "R" && ${{STATUS}} != "PD" && ${{STATUS}} != "S" && ${{STATUS}} != "CG" && ${{STATUS}} != "CF" ]]
        then
            FAILED=$((FAILED + 1))
        fi

        if [[ $COLLAPSED_TIME -gt $MAX_TIME ]]
        then
            MAX_TIME=$COLLAPSED_TIME
        fi

        JOB_STATUSES+=(${{STATUS}})
        JOB_EXECUTION_TIME+=(${{COLLAPSED_TIME}})
        echo "# `printf "%5d" $JOB_ID` `printf "%20s" $START_TIME` `printf "%20s" $END_TIME` `printf "%10s" $STATUS` `printf "%6s" $COLLAPSED_TIME`" >> ${{LOG_FILE}}
        echo " `printf "%5d" $JOB_ID` `printf "%20s" $START_TIME` `printf "%20s" $END_TIME` `printf "%10s" $STATUS` `printf "%6s" $COLLAPSED_TIME`"
    done
    echo "#" >> ${{LOG_FILE}}
}}


function writeTimeInSeconds(){{

    echo "###########################################################" >> ${{LOG_FILE}}
    echo "############### EXECUTION TIME IN SECONDS #################" >> ${{LOG_FILE}}
    echo "###########################################################" >> ${{LOG_FILE}}
    echo "#" >> ${{LOG_FILE}}
    echo "     ID                 TIME      STATUS                   " >> ${{LOG_FILE}}

    for i in `seq 1 $TASK_NUMBER`;
    do
        echo "  `printf "%5d" $i` `printf "%20d" ${{JOB_EXECUTION_TIME[(($i - 1))]}}`  `printf "%10s" ${{JOB_STATUSES[(($i - 1))]}}`" >> ${{LOG_FILE}}
    done
    echo "#" >> ${{LOG_FILE}}

}}

function writeJobsDetailInformation(){{
    for i in ${{WORKSPACE}}/job_*;
    do
        JOB_DIR_NAME=$(basename $i)
        if [[ $JOB_DIR_NAME =~ $JOB_ID_REGEX ]];
        then
            JOB_ID=${{BASH_REMATCH[1]}};

            # remove 0 at the beginning of the number
            JOB_ID=$(expr $JOB_ID + 0)
        else
            echo "Cannot get job ID from $i file"
            continue
        fi

        INFO_FILE=$i/$JOBS_LOG_FILE

        if [ ! -f $INFO_FILE ]; then
            continue
        fi

        EXECUTION_TIME=${{JOB_EXECUTION_TIME[(($JOB_ID - 1))]}}
        SIMULATION_STATUS=${{JOB_STATUSES[(($JOB_ID - 1))]}}

        cat $INFO_FILE | sed "7s/.*/# TIME IN SECONDS =`printf "%20d" $EXECUTION_TIME`/" | sed "9s/.*/# STATUS          =`printf "%20s" $SIMULATION_STATUS`/" >> ${{LOG_FILE}}

    done
}}

function writeSummary(){{
    echo "###########################################################" >> ${{LOG_FILE}}
    echo "######################## SUMMARY ##########################" >> ${{LOG_FILE}}
    echo "###########################################################" >> ${{LOG_FILE}}
    echo "#" >> ${{LOG_FILE}}
    echo "# NUMBER OF TASKS = `printf "%20d" $TASK_NUMBER`" >> ${{LOG_FILE}}
    echo "# SUCCESS         = `printf "%20d" $SUCCESSES`" >> ${{LOG_FILE}}
    echo "# FAILED          = `printf "%20d" $FAILED`" >> ${{LOG_FILE}}

    if [[ ${{SUCCESSES}} -ne 0 ]]
    then
        echo "# AVERAGE TIME [s]= `printf "%20d" $(($TOTAL_TIME / $SUCCESSES))`" >> ${{LOG_FILE}}
        echo "# MAX TIME [s]    = `printf "%20s" $MAX_TIME`" >> ${{LOG_FILE}}
    else
        echo "# AVERAGE TIME [s]= `printf "%20s" -`" >> ${{LOG_FILE}}
        echo "# MAX TIME [s]    = `printf "%20s" -`" >> ${{LOG_FILE}}
    fi

    echo "#" >> ${{LOG_FILE}}
}}

function appendCollectInfo() {{
    if [ -f $COLLECT_LOG ]; then
        cat $COLLECT_LOG >> ${{LOG_FILE}}
    fi
}}

WORKSPACE={workspace_dir:s}
MAIN_DIR={main_dir:s}
COLLECT_LOG={collect_dir:s}/info.log

if [ $# -eq 0 ]
  then
    FILE_NAME=status_`date +%Y%m%d_%H%M%S`.log
    LOG_FILE=${{MAIN_DIR}}/workspace/${{FILE_NAME}}
  else
    LOG_FILE=$1
fi

JOBS_LOG_FILE="info.log"
JOB_ID_REGEX="job_([0-9]*)"
START_REGEX="# START\s+=\s(.{{19}})"
END_REGEX="# END\s+=\s(.{{19}})"
STATUS_REGEX="# STATUS\s+=\s+([A-Z]*)"
COLLAPSED_TIME_REGEX="# TIME IN SECONDS\s+=\s+([0-9]*)"
TASK_NUMBER=0
SUCCESSES=0
FAILED=0
MAX_TIME=0
TOTAL_TIME=0
JOB_STATUSES=()
JOB_EXECUTION_TIME=()

LOGFILE="${{MAIN_DIR}}/submit.log"

RE="Job ID: ([0-9]*)"

# no log file. Probably submit.sh not run
if [ ! -f $LOGFILE ]; then
    echo "File not found: $LOGFILE"
    echo "Make sure you run submit script"
    exit 1
fi

if [[ $(cat $LOGFILE) =~ $RE ]];
then
    ARRAY_JOB_ID=${{BASH_REMATCH[1]}};
fi

writeLogHeader
writeTimeInSeconds
#writeJobsDetailInformation
appendCollectInfo
writeSummary

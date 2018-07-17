#!/usr/bin/env bash

# Exit immediately if a simple command exits with a non-zero status.
set -e

function writeLogHeader(){{
    echo "###########################################################" > ${{LOG_FILE}}
    echo "############ START AND END OF JOBS EXECUTION ##############" >> ${{LOG_FILE}}
    echo "###########################################################" >> ${{LOG_FILE}}
    echo "#" >> ${{LOG_FILE}}
    echo "#    ID                      START                      END" >> ${{LOG_FILE}}

    for i in ${{WORKSPACE}}/job_*/${{JOBS_LOG_FILE}};
    do
        if [[ $(cat $i) =~ $JOB_ID_REGEX ]];
        then
            JOB_ID=${{BASH_REMATCH[1]}};
        else
            echo "Cannot get job ID from $i file"
            continue
        fi

        if [[ $(cat $i) =~ $START_REGEX ]];
        then
            START_TIME=${{BASH_REMATCH[1]}};
        else
            echo "Cannot get start time from $i file"
            continue
        fi

        if [[ $(cat $i) =~ $END_REGEX ]];
        then
            END_TIME=${{BASH_REMATCH[1]}};
        else
            echo "Cannot get end time from $i file"
            continue
        fi

        if [[ $(cat $i) =~ $STATUS_REGEX ]];
        then
            STATUS=${{BASH_REMATCH[1]}};
        else
            echo "Cannot get status from $i file"
            continue
        fi

        echo "# `printf "%5d" $JOB_ID`        $START_TIME      $END_TIME" >> ${{LOG_FILE}}
    done
    echo "#" >> ${{LOG_FILE}}
}}

function writeTimeInSeconds(){{
    echo "###########################################################" >> ${{LOG_FILE}}
    echo "############### EXECUTION TIME IN SECONDS #################" >> ${{LOG_FILE}}
    echo "###########################################################" >> ${{LOG_FILE}}
    echo "#" >> ${{LOG_FILE}}
    echo "     ID                 TIME      STATUS                   " >> ${{LOG_FILE}}

    for i in ${{WORKSPACE}}/job_*/${{JOBS_LOG_FILE}};
    do
        if [[ $(cat $i) =~ $JOB_ID_REGEX ]];
        then
            JOB_ID=${{BASH_REMATCH[1]}};
        else
            echo "Cannot get job ID from $i file"
            continue
        fi

        if [[ $(cat $i) =~ $COLLAPSED_TIME_REGEX ]];
        then
            COLLAPSED_TIME=${{BASH_REMATCH[1]}};
        else
            echo "Cannot get collapsed time from $i file"
            continue
        fi

        if [[ $(cat $i) =~ $STATUS_REGEX ]];
        then
            STATUS=${{BASH_REMATCH[1]}};
        else
            echo "Cannot get status from $i file"
            continue
        fi

        TASK_NUMBER=$((TASK_NUMBER + 1))

        if [[ ${{STATUS}} -ne 0 ]]
        then
            FAILED=$((FAILED + 1))
        else
            SUCCESSES=$((SUCCESSES + 1))
            TOTAL_TIME=$((TOTAL_TIME + $COLLAPSED_TIME))
        fi

        echo "  `printf "%5d" $JOB_ID` `printf "%20d" $COLLAPSED_TIME`  `printf "%10d" $STATUS`" >> ${{LOG_FILE}}
    done
    echo "#" >> ${{LOG_FILE}}
}}

function writeJobsDetailInformation(){{
    cat ${{WORKSPACE}}/job_*/${{JOBS_LOG_FILE}} >> ${{LOG_FILE}}
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
    else
        echo "# AVERAGE TIME [s]= `printf "%20s" -`" >> ${{LOG_FILE}}
    fi

    echo "#" >> ${{LOG_FILE}}
}}

function appendCollectInfo() {{
    if [ -f $COLLECT_LOG ]; then
        cat $COLLECT_LOG >> ${{LOG_FILE}}
    fi
}}

JOBS_LOG_FILE="info.log"
WORKSPACE={workspace_dir:s}
LOG_FILE=${{WORKSPACE}}/${{JOBS_LOG_FILE}}
JOB_ID_REGEX="#+ DETAILED INFORMATION ABOUT JOB\s+([0-9]*)"
START_REGEX="# START\s+=\s(.{{19}})"
END_REGEX="# END\s+=\s(.{{19}})"
STATUS_REGEX="# STATUS\s+=\s+([0-9]*)"
COLLAPSED_TIME_REGEX="# TIME IN SECONDS\s+=\s+([0-9]*)"
COLLECT_LOG={collect_dir:s}/info.log
TASK_NUMBER=0
SUCCESSES=0
FAILED=0
TOTAL_TIME=0

writeLogHeader
writeTimeInSeconds
writeJobsDetailInformation
appendCollectInfo
writeSummary

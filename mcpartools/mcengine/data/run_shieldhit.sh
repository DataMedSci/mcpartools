#!/usr/bin/env bash

# Exit immediately if a simple command exits with a non-zero status.
set -e


START=$(date +%s)

# location of SHIELDHIT binary file
SHIELDHIT_BIN={shieldhit_bin:s}

# working directory, output files will be saved here
WORK_DIR={working_directory:s}

# number of particles per job
PARTICLE_NO={particle_no:d}

# seed of RNG
RNG_SEED={rnd_seed:d}

# main SHIELDHIT12A input files
BEAM_FILE={beam_file:s}
GEO_FILE={geo_file:s}
MAT_FILE={mat_file:s}
DETECT_FILE={detect_file:s}

LOG_FILE=$WORK_DIR"/info.log"

echo "###########################################################" > $LOG_FILE
echo "######### DETAILED INFORMATION ABOUT JOB `printf "%5d" $RNG_SEED` ############" >> $LOG_FILE
echo "###########################################################" >> $LOG_FILE
echo "#" >> $LOG_FILE
echo "# START           = `date +"%Y-%m-%d %H:%M:%S"`" >> $LOG_FILE
echo "# END             =                   -" >> $LOG_FILE
echo "# TIME IN SECONDS =                   -" >> $LOG_FILE
echo "# NO OF PARTICLES =`printf "%20d" $PARTICLE_NO`" >> $LOG_FILE
echo "# STATUS          =                   1" >> $LOG_FILE
echo "#" >> $LOG_FILE

# execute simulation
$SHIELDHIT_BIN --beamfile=$BEAM_FILE --geofile=$GEO_FILE --matfile=$MAT_FILE --detectfile=$DETECT_FILE -n $PARTICLE_NO -N $RNG_SEED {engine_options:s} $WORK_DIR
SIMULATION_STATUS=$?

let "EXECUTION_TIME = $(date +%s) - $START"

#    end time is in line number 6
sed -i "6s/.*/# END             = `date +"%Y-%m-%d %H:%M:%S"`/" $LOG_FILE
#    collapsed time is in line number 7
sed -i "7s/.*/# TIME IN SECONDS =`printf "%20d" $EXECUTION_TIME`/" $LOG_FILE
#    status is in line number 9
sed -i "9s/.*/# STATUS          =`printf "%20d" $SIMULATION_STATUS`/" $LOG_FILE
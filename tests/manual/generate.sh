#!/usr/bin/env bash

set -e # Exit immediately if a simple command exits with a non-zero status.

if [[ $# -ne 1 ]] ; then
    echo "Correct usage: generate.sh path_to_mcpartools"
    exit 1
fi

MAIN_DIR=$1

pip install versioneer

cd $MAIN_DIR
versioneer install
PYTHONPATH=$MAIN_DIR python $MAIN_DIR/mcpartools/generatemc.py --help

PYTHONPATH=$MAIN_DIR python $MAIN_DIR/mcpartools/generatemc.py -j 5 -p 10000 $MAIN_DIR/tests/res/shieldhit -w shieldhit

PYTHONPATH=$MAIN_DIR python $MAIN_DIR/mcpartools/generatemc.py -j 5 -p 10000 $MAIN_DIR/tests/res/sample_fluka.inp -w fluka

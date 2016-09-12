#!/usr/bin/env bash

set -e # Exit immediately if a simple command exits with a non-zero status.

if [[ $# -ne 1 ]] ; then
    echo "Correct usage: generate.sh path_to_mcpartools"
    exit 1
fi

MAIN_DIR=$1

$MAIN_DIR/fluka/run_*/collect.sh
ls $MAIN_DIR/fluka/run_*/output/*fort*

$MAIN_DIR/shieldhit/run_*/collect.sh
ls $MAIN_DIR/shieldhit/run_*/output/*bdo

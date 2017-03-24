#!/usr/bin/env bash

qsub {options_args:s} -t 1-{jobs_no:d} -o {log_dir:s} -e {log_dir:s} {script_path:s}

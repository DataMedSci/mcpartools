#!/usr/bin/env bash
qsub {options_args:s} -t 1-{jobs_no:d} {script_path:s}

#!/usr/bin/env bash
{options_header:s}
qsub {options_args:s} -t 1-{jobs_no:d} {script_path:s}

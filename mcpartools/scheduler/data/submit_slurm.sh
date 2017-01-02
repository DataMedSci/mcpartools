#!/bin/bash
sbatch {options_args:s} --array=1-{jobs_no:d} {script_path:s}

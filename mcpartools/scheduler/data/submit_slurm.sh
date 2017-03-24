#!/bin/bash
sbatch {options_args:s} --array=1-{jobs_no:d} --output="{log_dir:s}/output_%j_%a.log" --error="{log_dir:s}/error_%j_%a.log" {script_path:s}

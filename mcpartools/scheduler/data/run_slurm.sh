#!/usr/bin/env bash
{workspace_dir:s}/job_`printf %04d $SLURM_ARRAY_TASK_ID`/run.sh
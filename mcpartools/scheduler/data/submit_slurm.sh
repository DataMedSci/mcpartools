#!/bin/bash
{:s}
sbatch -A ccbmc5 -p plgrid --time=1:00:00 --array=1-{:d} {:s}

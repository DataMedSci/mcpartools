#!/usr/bin/env bash
# go to working directory
cd {working_directory:s}
# run rfluka
rfluka -N0 -M1 {input_basename:s}
# rename output files, appeding suffix
for f in {input_basename:s}001*; do mv $f {input_basename:s}{job_id:04d}${{f#{input_basename:s}001}}; done
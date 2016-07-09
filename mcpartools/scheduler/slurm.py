import os

from mcpartools.scheduler.base import JobScheduler


class Slurm(JobScheduler):
    pass

    submit_script_template = """#!/bin/bash
sbatch -A ccbmc5 -p plgrid --time=1:00:00 --array=1-{:d} {:s}
"""

    main_run_script_template = """#!/bin/bash
./job_$SLURM_ARRAY_TASK_ID/run.sh
"""

    def submit_script_body(self, particle_no, workspace_dir):
        script_path = os.path.join(workspace_dir, "main_run.sh")
        return self.submit_script_template.format(particle_no, script_path)

    def main_run_script_body(self):
        # TODO fix it
        return self.main_run_script_template

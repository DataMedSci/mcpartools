from mcpartools.scheduler.base import JobScheduler


class Slurm(JobScheduler):
    pass

    submit_script_template = """#!/bin/bash
sbatch -A ccbmc5 -p plgrid --time=1:00:00 --array=1-{:d} workspace/run.sh
"""

    main_run_script_template = """#!/bin/bash
./job_$SLURM_ARRAY_TASK_ID/run.sh
"""

    def submit_script_body(self, particle_no):
        return self.submit_script_template.format(particle_no)

    def main_run_script_body(self):
        # TODO fix it
        return self.main_run_script_template

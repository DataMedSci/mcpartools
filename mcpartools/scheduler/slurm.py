from mcpartools.scheduler.base import JobScheduler


class Slurm(JobScheduler):
    pass

    submit_script_template = """#!/bin/bash
sbatch --array=1-{:d} workspace/run.sh
"""

    main_run_script_template = """#!/bin/bash
run_$SLURM_ID
"""

    def submit_script_body(self, particle_no):
        return self.submit_script_template.format(particle_no)

    def main_run_script_body(self):
        #TODO fix it
        return self.main_run_script_template

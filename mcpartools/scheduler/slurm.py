import os

from mcpartools.scheduler.base import JobScheduler


class Slurm(JobScheduler):

    id = "slurm"

    def __init__(self, options_content):
        JobScheduler.__init__(self, options_content)

    submit_script_template = os.path.join('data', 'submit_slurm.sh')
    smart_submit_script_template = os.path.join('data', 'smart_submit_slurm.sh.j2')

    main_run_script_template = os.path.join('data', 'run_slurm.sh')

import os

from mcpartools.scheduler.base import JobScheduler


class Slurm(JobScheduler):

    def __init__(self, options_content):
        JobScheduler.__init__(self, options_content)

    submit_script_template = os.path.join('data', 'submit_slurm.sh')

    main_run_script_template = os.path.join('data', 'run_slurm.sh')

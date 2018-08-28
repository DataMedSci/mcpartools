import os

from mcpartools.scheduler.base import JobScheduler


class Slurm(JobScheduler):

    id = "slurm"

    def __init__(self, options_content):
        JobScheduler.__init__(self, options_content)

    submit_script_template = os.path.join('data', 'submit_slurm.sh')

    main_run_script_template = os.path.join('data', 'run_slurm.sh')

    merge_logs_script_template = os.path.join('data', 'merge_logs.sh')

    status_script_template = os.path.join('data', 'status.sh')

    kill_script_template = os.path.join('data', 'kill_slurm.sh')

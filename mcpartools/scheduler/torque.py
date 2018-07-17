import os

from mcpartools.scheduler.base import JobScheduler


class Torque(JobScheduler):

    id = "torque"

    def __init__(self, options_content):
        JobScheduler.__init__(self, scheduler_options=options_content)

    submit_script_template = os.path.join('data', 'submit_torque.sh')

    main_run_script_template = os.path.join('data', 'run_torque.sh')

    merge_logs_script_template = os.path.join('data', 'merge_logs_torque.sh')

    status_script_template = os.path.join('data', 'status.sh')

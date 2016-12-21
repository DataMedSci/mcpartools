import os

from mcpartools.scheduler.base import JobScheduler


class Torque(JobScheduler):
    def __init__(self, options_content):
        JobScheduler.__init__(self, scheduler_options=options_content)

    @staticmethod
    def id():
        return "torque"

    submit_script_template = os.path.join('data', 'submit_torque.sh')

    main_run_script_template = os.path.join('data', 'run_torque.sh')

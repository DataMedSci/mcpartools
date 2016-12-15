import os

from mcpartools.scheduler.base import JobScheduler


class Torque(JobScheduler):
    def __init__(self, options_content):
        JobScheduler.__init__(self, scheduler_options=options_content)

        submit_torque_script = os.path.join('data', 'submit_torque.sh')

        run_torque_script = os.path.join('data', 'run_torque.sh')

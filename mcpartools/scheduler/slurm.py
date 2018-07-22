import os

from mcpartools.scheduler.base import JobScheduler


class Slurm(JobScheduler):

    id = "slurm"

    def __init__(self, options_content, dump_opt):
        JobScheduler.__init__(self, scheduler_options=options_content, dump_opt=dump_opt)

    submit_script_template = os.path.join('data', 'submit_slurm.sh')

    main_run_script_template = os.path.join('data', 'run_slurm.sh')

    dump_script_template = os.path.join('data', 'dump_slurm.sh')

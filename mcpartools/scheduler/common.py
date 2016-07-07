from mcpartools.scheduler.slurm import Slurm


class SchedulerDiscover:
    def __init__(self):
        pass

    @classmethod
    def get_scheduler(cls):
        return Slurm()

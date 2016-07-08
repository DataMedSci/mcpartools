import logging

from mcpartools.scheduler.slurm import Slurm

logger = logging.getLogger(__name__)


class SchedulerDiscover:
    def __init__(self):
        pass

    @classmethod
    def get_scheduler(cls):
        logger.debug("Discovered job scheduler SLURM")
        return Slurm()

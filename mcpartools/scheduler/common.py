import logging
import os
from subprocess import check_call, CalledProcessError

from mcpartools.scheduler.slurm import Slurm
from mcpartools.scheduler.torque import Torque

logger = logging.getLogger(__name__)


class SchedulerDiscover:
    supported = (Torque, Slurm)

    def __init__(self):
        pass

    @classmethod
    def get_scheduler(cls, scheduler_options, log_location):
        with open(os.path.join(log_location, "generatemc.log"), 'w+') as LOG_FILE:
            try:
                check_call(['srun --version'], stdout=LOG_FILE, stderr=LOG_FILE, shell=True)
                logger.debug("Discovered job scheduler SLURM")
                return Slurm(scheduler_options)
            except CalledProcessError as e:
                logger.debug("Slurm not found: %s", e)
            try:
                check_call(['qsub --version'], stdout=LOG_FILE, stderr=LOG_FILE, shell=True)
                logger.debug("Discovered job scheduler Torque")
                return Torque(scheduler_options)
            except CalledProcessError as e:
                logger.debug("Torque not found: %s", e)
        raise SystemError("No known batch system found!")

import logging
import os
from subprocess import check_call, CalledProcessError

from mcpartools.scheduler.slurm import Slurm
from mcpartools.scheduler.torque import Torque

logger = logging.getLogger(__name__)


class SchedulerDiscover:
    def __init__(self):
        pass

    @classmethod
    def get_scheduler(cls, scheduler_options):
        with open(os.devnull, 'w') as FNULL:
            try:
                check_call(['srun --version'], stdout=FNULL, shell=True)
                check_call(['sinfo --help'], stdout=FNULL, shell=True)
                logger.debug("Discovered job scheduler SLURM")
                return Slurm(scheduler_options)
            except CalledProcessError as e:
                logger.debug("Slurm not found: %s", e)
            try:
                check_call(['man qsub'], stdout=FNULL, shell=True)
                check_call(['qstat -B'], stdout=FNULL, shell=True)
                logger.debug("Discovered job scheduler Torque")
                return Torque(scheduler_options)
            except CalledProcessError as e:
                logger.debug("Torque not found: %s", e)
        raise SystemError("No known batch system found!")
import logging
from subprocess import check_call, CalledProcessError

from mcpartools.scheduler.slurm import Slurm
from mcpartools.scheduler.torque import Torque

logger = logging.getLogger(__name__)


class SchedulerDiscover:
    def __init__(self):
        pass

    @classmethod
    def get_scheduler(cls, scheduler_options):
        try:
            check_call(['srun', '--version'], shell=True)
            check_call(['sinfo', '--help'], shell=True)
            logger.debug("Discovered job scheduler SLURM")
            return Slurm(scheduler_options)
        except CalledProcessError as e:
            print("Slurm not found: ", str(e))
        try:
            check_call(['qstat', '-B'])
            logger.debug("Discovered job scheduler Torque")
            return Torque(scheduler_options)
        except CalledProcessError as e:
            print("Torque not found: ", str(e))
        raise SystemError("No known batch system found!")

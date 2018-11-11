import logging
from subprocess import check_output, CalledProcessError

from mcpartools.scheduler.slurm import Slurm
from mcpartools.scheduler.torque import Torque

logger = logging.getLogger(__name__)


class SchedulerDiscover:
    supported = (Torque, Slurm)

    def __init__(self):
        pass

    @classmethod
    def get_scheduler(cls, scheduler_options, log_location):
        file_logger = logging.getLogger('file_logger')
        try:
            srun_output = check_output(['srun --version'], shell=True)
            file_logger.info("srun version: {}".format(srun_output[:-1]))
            logger.debug("Discovered job scheduler SLURM")
            return Slurm(scheduler_options)
        except CalledProcessError as e:
            logger.debug("Slurm not found: %s", e)
        try:
            qsub_output = check_output(['qsub --version'], shell=True)
            file_logger.info("qsub version: {}".format(qsub_output[:-1]))
            logger.debug("Discovered job scheduler Torque")
            return Torque(scheduler_options)
        except CalledProcessError as e:
            logger.debug("Torque not found: %s", e)
        raise SystemError("No known batch system found!")

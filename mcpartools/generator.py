import os
import logging
import time

from mcpartools.mcengine.common import EngineDiscover
from mcpartools.scheduler.common import SchedulerDiscover

logger = logging.getLogger(__name__)


class Options:
    def __init__(self, args):
        self._valid = True

        # TODO add check if > 1
        self.particle_no = args.particle_no

        # TODO add check if > 0
        self.jobs_no = args.jobs_no

        self.input_path = args.input
        if not os.path.exists(self.input_path):
            logging.error("Input path " + self.input_path + " doesn't exists")
            self._valid = False

        if os.path.isdir(self.input_path):
            self.root_dir = self.input_path
        else:
            self.root_dir = os.path.dirname(self.input_path)
        logger.debug("Root directory: " + self.root_dir)

    @property
    def valid(self):
        return self._valid


class Generator:
    def __init__(self, options):
        self.options = options
        print("number of particles", options.particle_no)
        print("number of jobs", options.jobs_no)
        self.scheduler = SchedulerDiscover.get_scheduler()
        self.mc_engine = EngineDiscover.get_mcengine(self.options.input_path)

    def run(self):
        if not self.options.valid:
            logging.error("Invalid options, aborting run")
            return

        # generate main dir according to date
        self.generate_main_dir()

        # generate submit script
        self.generate_submit_script()

        # generate tmp dir with workspace
        self.generate_workspace()

        # copy input files
        self.copy_input()

        # save logs
        self.save_logs()

    def generate_main_dir(self):
        dir_name = time.strftime("run_%Y%m%d_%H%M%S")
        logger.debug("Generated main directory name: " + dir_name)

        dir_path = os.path.join(self.options.root_dir, dir_name)
        logger.debug("Generated main directory path: " + dir_path)

        os.mkdir(dir_path)
        self.main_dir = dir_path

    def generate_submit_script(self):
        script_path = os.path.join(self.main_dir, self.scheduler.submit_script)
        self.scheduler.write_submit_script(script_path,
                                           self.options.particle_no)

    def generate_workspace(self):
        wspdir_name = 'workspace'
        wspdir_path = os.path.join(self.main_dir, wspdir_name)
        logger.debug("Generated workspace directory path: " + wspdir_path)
        os.mkdir(wspdir_path)
        self.workspace_dir = wspdir_path

        for jobid in range(self.options.jobs_no):
            print(jobid)
            # TODO add padding with zeros
            jobdir_name = "job_{:d}".format(jobid)
            logger.debug("Generated job directory name: " + jobdir_name)
            jobdir_path = os.path.join(self.workspace_dir, jobdir_name)
            os.mkdir(jobdir_path)
            logger.debug("Generated job directory path: " + jobdir_path)

    def copy_input(self):
        indir_name = 'input'
        indir_path = os.path.join(self.main_dir, indir_name)
        logger.debug("Generated input directory path: " + indir_path)
        os.mkdir(indir_path)
        self.input_dir = indir_path

    def save_logs(self):
        pass

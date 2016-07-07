import os
import logging
import time

from mcpartools.scheduler.common import SchedulerDiscover

logger = logging.getLogger(__name__)


class Options:
    def __init__(self, args):
        self._valid = True
        self.particle_no = args.particle_no
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
        pass

    def copy_input(self):
        pass

    def save_logs(self):
        pass

import os
import logging
import shutil
import time

from mcpartools.mcengine.common import EngineDiscover
from mcpartools.scheduler.common import SchedulerDiscover

logger = logging.getLogger(__name__)


class Options:
    def __init__(self, args):
        self._valid = True

        self.particle_no = args.particle_no
        if self.particle_no < 1:
            logger.error("Number of particles should be positive integer "
                         "(got " + str(self.particle_no) + " instead")
            self._valid = False

        self.jobs_no = args.jobs_no
        if self.jobs_no < 1:
            logger.error("Number of jobs should be positive integer "
                         "(got " + str(self.jobs_no) + " instead")
            self._valid = False

        self.input_path = args.input
        if not os.path.exists(self.input_path):
            logger.error("Input path " + str(self.input_path) +
                         " doesn't exists")
            self._valid = False

        if os.path.isdir(self.input_path):
            self.root_dir = self.input_path
        else:
            self.root_dir = os.path.dirname(self.input_path)
        logger.debug("Root directory: " + str(self.root_dir))

        self.mc_run_template = args.mc_run_template
        if self.mc_run_template is not None and \
                not os.path.exists(self.mc_run_template):
            logging.error("MC run template " + self.mc_run_template +
                          " doesn't exists")
            self._valid = False

        self.scheduler_options = args.scheduler_options

    @property
    def valid(self):
        return self._valid


class Generator:
    def __init__(self, options):
        self.options = options
        self.scheduler = SchedulerDiscover.get_scheduler(
            self.options.scheduler_options
        )
        self.mc_engine = EngineDiscover.get_mcengine(
            self.options.input_path,
            self.options.mc_run_template)

    def run(self):
        if not self.options.valid:
            logger.error("Invalid options, aborting run")
            return

        # generate main dir according to date
        self.generate_main_dir()

        # generate tmp dir with workspace
        self.generate_workspace()

        # generate submit script
        self.generate_submit_script()

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

    def generate_workspace(self):
        wspdir_name = 'workspace'
        wspdir_path = os.path.join(self.main_dir, wspdir_name)
        logger.debug("Generated workspace directory path: " + wspdir_path)
        os.mkdir(wspdir_path)
        self.workspace_dir = wspdir_path

        for jobid in range(self.options.jobs_no):
            jobdir_name = "job_{:04d}".format(jobid + 1)
            logger.debug("Generated job directory name: " + jobdir_name)
            jobdir_path = os.path.join(self.workspace_dir, jobdir_name)
            os.mkdir(jobdir_path)
            logger.debug("Generated job directory path: " + jobdir_path)

            self.mc_engine.randomize(jobid + 1)
            self.mc_engine.set_particle_no(self.options.particle_no)
            self.mc_engine.save_input(jobdir_path)

            self.mc_engine.save_run_script(jobdir_path, jobid + 1)

        self.scheduler.write_main_run_script(self.workspace_dir)
        self.mc_engine.write_collect_script(self.main_dir)

    def generate_submit_script(self):
        script_path = os.path.join(self.main_dir, self.scheduler.submit_script)
        logger.debug("Preparation to generate " + script_path)
        logger.debug("Jobs no " + str(self.options.jobs_no))
        self.scheduler.write_submit_script(script_path,
                                           self.options.jobs_no,
                                           self.workspace_dir)

    def copy_input(self):
        indir_name = 'input'
        indir_path = os.path.join(self.main_dir, indir_name)
        logger.debug("Generated input directory path: " + indir_path)
        os.mkdir(indir_path)
        self.input_dir = indir_path

        for f in self.mc_engine.input_files:
            f_base_name = os.path.basename(f)
            dest_file = os.path.join(self.input_dir, f_base_name)
            logger.debug("Copying " + f + " to " + dest_file)
            shutil.copyfile(f, dest_file)

    def save_logs(self):
        pass

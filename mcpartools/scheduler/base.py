import logging
import os

logger = logging.getLogger(__name__)


class JobScheduler:
    def __init__(self, options_file_path):
        self.options_file_path = options_file_path

    submit_script = 'submit.sh'

    def write_submit_script(self, script_path, jobs_no, workspace_dir):
        fd = open(script_path, 'w')
        abs_path_workspace = os.path.abspath(workspace_dir)
        fd.write(self.submit_script_body(jobs_no, abs_path_workspace))
        fd.close()
        os.chmod(script_path, 0o750)
        logger.debug("Saved submit script: " + script_path)
        logger.debug("Jobs no " + str(jobs_no))
        logger.debug("Workspace " + abs_path_workspace)

    def write_main_run_script(self, output_dir):
        out_file_name = "main_run.sh"
        out_file_path = os.path.join(output_dir, out_file_name)
        output_dir_abs_path = os.path.abspath(output_dir)
        fd = open(out_file_path, 'w')
        fd.write(self.main_run_script_body(output_dir_abs_path))
        fd.close()
        os.chmod(out_file_path, 0o750)
        logger.debug("Saved main run script: " + out_file_path)
        logger.debug("Output dir " + output_dir)

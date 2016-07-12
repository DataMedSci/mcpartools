import logging
import os

logger = logging.getLogger(__name__)


class JobScheduler:
    def __init__(self, scheduler_options):
        # check if user provided path to options file
        if scheduler_options is None:
            self.options_header = "# no user options provided"
            self.options_args = ""
        elif os.path.exists(scheduler_options):
            opt_fd = open(scheduler_options, 'r')
            options_file_content = opt_fd.read()
            opt_fd.close()
            self.options_header = options_file_content
            self.options_args = ""
        else:
            self.options_header = "# no user options provided"
            self.options_args = scheduler_options

    submit_script = 'submit.sh'
    main_run_script = 'main_run.sh'

    def submit_script_body(self, jobs_no, workspace_dir):
        from pkg_resources import resource_string
        tpl = resource_string(__name__, self.submit_script_template)
        self.submit_script = tpl.decode('ascii')

        script_path = os.path.join(workspace_dir, "main_run.sh")

        return self.submit_script.format(options_header=self.options_header,
                                         options_args=self.options_args,
                                         jobs_no=jobs_no,
                                         script_path=script_path)

    def main_run_script_body(self, workspace_dir):
        from pkg_resources import resource_string
        tpl = resource_string(__name__, self.main_run_script_template)
        self.main_run_script = tpl.decode('ascii').format(
            workspace_dir=workspace_dir)

        return self.main_run_script

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
        output_dir_abspath = os.path.abspath(output_dir)
        out_file_path = os.path.join(output_dir_abspath, self.main_run_script)
        fd = open(out_file_path, 'w')
        fd.write(self.main_run_script_body(output_dir_abspath))
        fd.close()
        os.chmod(out_file_path, 0o750)
        logger.debug("Saved main run script: " + out_file_path)
        logger.debug("Output dir " + output_dir)

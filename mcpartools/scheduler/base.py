import logging
import os

logger = logging.getLogger(__name__)


class JobScheduler:
    def __init__(self, scheduler_options):
        # check if user provided path to options file
        if scheduler_options is None:
            self.options_header = "# no user options provided"
            self.options_args = ""
            logger.debug("No scheduler options")
        elif os.path.exists(scheduler_options):
            with open(scheduler_options, 'r') as f:
                options_file_content = f.read()
                self.options_header = options_file_content
                logger.debug("Scheduler options file:" + options_file_content)
            self.options_args = ""
        else:
            self.options_header = "# no user options provided"
            self.options_args = scheduler_options[1:-1]
            logger.debug("Scheduler options argument:" + self.options_args)

    submit_script = 'submit.sh'
    main_run_script = 'main_run.sh'

    def submit_script_body(self, jobs_no, workspace_dir):
        from pkg_resources import resource_string
        tpl = resource_string(__name__, self.submit_script_template)
        self.submit_script = tpl.decode('ascii')

        log_dir = os.path.join(workspace_dir, "log")
        if not os.path.exists(log_dir):
            os.mkdir(log_dir)

        script_path = os.path.join(workspace_dir, "main_run.sh")

        return self.submit_script.format(options_args=self.options_args,
                                         jobs_no=jobs_no,
                                         log_dir=log_dir,
                                         script_path=script_path)

    def main_run_script_body(self, jobs_no, workspace_dir):
        from pkg_resources import resource_string
        tpl = resource_string(__name__, self.main_run_script_template)
        self.main_run_script = tpl.decode('ascii').format(options_header=self.options_header,
                                                          workspace_dir=workspace_dir,
                                                          jobs_no=jobs_no)
        return self.main_run_script

    def write_submit_script(self, script_path, jobs_no, workspace_dir):
        abs_path_workspace = os.path.abspath(workspace_dir)
        with open(script_path, 'w') as f:
            f.write(self.submit_script_body(jobs_no, abs_path_workspace))
        os.chmod(script_path, 0o750)
        logger.debug("Saved submit script: " + script_path)
        logger.debug("Jobs no " + str(jobs_no))
        logger.debug("Workspace " + abs_path_workspace)

    def write_main_run_script(self, jobs_no, output_dir):
        output_dir_abspath = os.path.abspath(output_dir)
        out_file_path = os.path.join(output_dir_abspath, self.main_run_script)
        with open(out_file_path, 'w') as f:
            f.write(self.main_run_script_body(jobs_no=jobs_no, workspace_dir=output_dir_abspath))
        os.chmod(out_file_path, 0o750)
        logger.debug("Saved main run script: " + out_file_path)
        logger.debug("Output dir " + output_dir)

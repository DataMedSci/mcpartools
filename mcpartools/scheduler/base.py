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
            opt_fd = open(scheduler_options, 'r')
            options_file_content = opt_fd.read()
            opt_fd.close()
            self.options_header = options_file_content
            self.options_args = ""
            logger.debug("Scheduler options file:" + options_file_content)
        else:
            self.options_header = "# no user options provided"
            self.options_args = scheduler_options[1:-1]
            logger.debug("Scheduler options argument:" + self.options_args)

    submit_script = 'submit.sh'
    main_run_script = 'main_run.sh'
    merge_logs_script = 'merge_logs.sh'
    status_script = 'status.sh'

    def submit_script_body(self, jobs_no, main_dir, workspace_dir):
        from pkg_resources import resource_string
        tpl = resource_string(__name__, self.submit_script_template)
        self.submit_script = tpl.decode('ascii')

        log_dir = os.path.join(main_dir, "log")
        if not os.path.exists(log_dir):
            os.mkdir(log_dir)

        return self.submit_script.format(options_args=self.options_args,
                                         jobs_no=jobs_no,
                                         log_dir=log_dir,
                                         script_dir=workspace_dir,
                                         calculate_script_name='main_run.sh',
                                         main_dir=main_dir,
                                         collect_script_name='collect.sh')

    def main_run_script_body(self, jobs_no, workspace_dir):
        from pkg_resources import resource_string
        tpl = resource_string(__name__, self.main_run_script_template)
        self.main_run_script = tpl.decode('ascii').format(options_header=self.options_header,
                                                          workspace_dir=workspace_dir,
                                                          jobs_no=jobs_no)
        return self.main_run_script

    def merge_logs_body(self, workspace_dir, collect_dir, main_dir):
        from pkg_resources import resource_string
        tpl = resource_string(__name__, self.merge_logs_script_template)
        return tpl.decode("ascii").format(workspace_dir=workspace_dir,
                                          collect_dir=collect_dir,
                                          main_dir=main_dir)

    def status_body(self, merge_script_path):
        from pkg_resources import resource_string
        tpl = resource_string(__name__, self.status_script_template)
        return tpl.decode("ascii").format(merge_script_path=merge_script_path)

    def write_submit_script(self, main_dir, script_basename, jobs_no, workspace_dir):
        script_path = os.path.join(main_dir, script_basename)
        fd = open(script_path, 'w')
        abs_path_workspace = os.path.abspath(workspace_dir)
        abs_path_main_dir = os.path.abspath(main_dir)
        fd.write(self.submit_script_body(jobs_no, abs_path_main_dir, abs_path_workspace))
        fd.close()
        os.chmod(script_path, 0o750)
        logger.debug("Saved submit script: " + script_path)
        logger.debug("Jobs no " + str(jobs_no))
        logger.debug("Workspace " + abs_path_workspace)

    def write_main_run_script(self, jobs_no, output_dir):
        output_dir_abspath = os.path.abspath(output_dir)
        out_file_path = os.path.join(output_dir_abspath, self.main_run_script)
        fd = open(out_file_path, 'w')
        fd.write(self.main_run_script_body(jobs_no=jobs_no, workspace_dir=output_dir_abspath))
        fd.close()
        os.chmod(out_file_path, 0o750)
        logger.debug("Saved main run script: " + out_file_path)
        logger.debug("Output dir " + output_dir)

    def write_merge_logs_script(self, workspace_dir, collect_dir, main_dir):
        workspace_dir_abspath = os.path.abspath(workspace_dir)
        collect_dir_abspath = os.path.abspath(collect_dir)
        main_dir_abspath = os.path.abspath(main_dir)

        out_file_path = os.path.join(workspace_dir_abspath, self.merge_logs_script)

        fd = open(out_file_path, 'w')
        fd.write(self.merge_logs_body(workspace_dir_abspath, collect_dir_abspath, main_dir_abspath))
        fd.close()
        os.chmod(out_file_path, 0o750)
        logger.debug("Saved merge logs script: " + out_file_path)

    def write_status_script(self, main_dir, workspace_dir):
        main_dir_abspath = os.path.abspath(main_dir)
        out_file_path = os.path.join(main_dir_abspath, self.status_script)

        workspace_dir_abspath = os.path.abspath(workspace_dir)
        merge_log_script = os.path.join(workspace_dir_abspath, self.merge_logs_script)

        fd = open(out_file_path, 'w')
        fd.write(self.status_body(merge_log_script))
        fd.close()
        os.chmod(out_file_path, 0o750)
        logger.debug("Saved status script: " + out_file_path)

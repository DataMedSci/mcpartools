import os

from mcpartools.scheduler.base import JobScheduler


class Slurm(JobScheduler):

    def __init__(self, options_file_path):
        super().__init__(options_file_path)
        if options_file_path is None:
            self.options_file_content = "# no user options provided"
        else:
            opt_fd = open(self.options_file_path, 'r')
            self.options_file_content = opt_fd.read()
            opt_fd.close()

    submit_script_template = os.path.join('data', 'submit_slurm.sh')

    main_run_script_template = os.path.join('data', 'run_slurm.sh')

    def submit_script_body(self, particle_no, workspace_dir):
        from pkg_resources import resource_string
        tpl = resource_string(__name__, self.submit_script_template)
        self.submit_script = tpl.decode('ascii')

        script_path = os.path.join(workspace_dir, "main_run.sh")

        return self.submit_script.format(self.options_file_content,
                                         particle_no, script_path)

    def main_run_script_body(self):
        from pkg_resources import resource_string
        tpl = resource_string(__name__, self.main_run_script_template)
        self.main_run_script = tpl.decode('ascii')

        return self.main_run_script

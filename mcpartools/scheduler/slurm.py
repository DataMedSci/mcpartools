from mcpartools.scheduler.base import JobScheduler


class Slurm(JobScheduler):
    pass

    submit_script_template = """sbatch --array=1-{} run.sh
    """

    def submit_script_body(self, particle_no):
        return self.submit_script_template.format(particle_no)

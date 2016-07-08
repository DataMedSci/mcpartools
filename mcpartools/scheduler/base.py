import logging
import os

logger = logging.getLogger(__name__)


class JobScheduler:
    def __init__(self):
        pass

    submit_script = 'submit.sh'

    def write_submit_script(self, script_path, particle_no):
        fd = open(script_path, 'w')
        fd.write(self.submit_script_body(particle_no))
        logging.debug("Saved submit script: " + script_path)

    def write_main_run_script(self, output_dir):
        out_file_name = "main_run.sh"
        out_file_path = os.path.join(output_dir, out_file_name)
        fd = open(out_file_path, 'w')
        fd.write(self.main_run_script_body())
        logging.debug("Saved main run script: " + out_file_path)

import logging

logger = logging.getLogger(__name__)


class JobScheduler:
    def __init__(self):
        pass

    submit_script = 'submit.sh'

    def write_submit_script(self, script_path, particle_no):
        f = open(script_path, 'w')

        f.write(self.submit_script_body(particle_no))
        logging.debug("Saved submit script: " + script_path)

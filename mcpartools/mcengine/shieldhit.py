import logging
import os
from pkg_resources import resource_string

from mcpartools.mcengine.mcengine import Engine

logger = logging.getLogger(__name__)


class ShieldHit(Engine):

    default_run_script_path = os.path.join('data', 'run_shieldhit.sh')
    collect_script = os.path.join('data', 'collect_shieldhit.sh')

    def __init__(self, input_path, mc_run_script):
        Engine.__init__(self, input_path, mc_run_script)

        # user didn't provided path to input scripts, use default
        if self.run_script_path is None:
            tpl = resource_string(__name__, self.default_run_script_path)
            self.run_script_content = tpl.decode('ascii')
            logger.debug("Using default run script: " + self.default_run_script_path)
        else:
            tpl_fd = open(self.run_script_path, 'r')
            self.run_script_content = tpl_fd.read()
            tpl_fd.close()
            logger.debug("Using user run script: " + self.run_script_path)

        self.collect_script_content = resource_string(__name__, self.collect_script).decode('ascii')

        self.particle_no = 1
        self.rng_seed = 1

    @property
    def input_files(self):
        base = os.path.abspath(self.input_path)
        # TODO add *.txt files with stopping power
        # TODO add *.ctx/.hed files with CT scans
        files = ('beam.dat', 'geo.dat', 'mat.dat', 'detect.dat')
        result = (os.path.join(base, f) for f in files)
        return result

    def randomize(self, new_seed, output_dir=None):
        self.rng_seed = new_seed

    def set_particle_no(self, particle_no):
        self.particle_no = particle_no

    def save_input(self, output_dir):
        logger.info("input files are not modified, we will used shieldhit switches instead")

    def save_run_script(self, output_dir, job_id):
        beam_file, geo_file, mat_file, detect_file = self.input_files
        abs_output_dir = os.path.abspath(output_dir)
        contents = self.run_script_content.format(
            shieldhit_bin='shieldhit',
            working_directory=abs_output_dir,
            particle_no=self.particle_no,
            rnd_seed=self.rng_seed,
            beam_file=beam_file,
            geo_file=geo_file,
            mat_file=mat_file,
            detect_file=detect_file
        )
        out_file_name = "run.sh"
        out_file_path = os.path.join(output_dir, out_file_name)
        out_fd = open(out_file_path, 'w')
        out_fd.write(contents)
        out_fd.close()
        os.chmod(out_file_path, 0o750)

    def write_collect_script(self, output_dir):
        output_dir_abs_path = os.path.abspath(output_dir)
        contents = self.collect_script_content.format(output_dir=output_dir_abs_path)
        out_file_name = "collect.sh"
        out_file_path = os.path.join(output_dir, out_file_name)
        out_fd = open(out_file_path, 'w')
        out_fd.write(contents)
        out_fd.close()
        os.chmod(out_file_path, 0o750)

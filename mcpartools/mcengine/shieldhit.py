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

    def parse_input_files(self):
        beam_file, geo_file, mat_file, detect_file = self.input_files
        # abs_output_dir = os.path.abspath(output_dir)
        external_beam_files = self._parse_beam_file(beam_file)
        logger.debug("External files found in BEAM file: %s" % external_beam_files)
        icru_numbers = self._parse_mat_file(mat_file)
        logger.debug("ICRUs found in MAT file: %s" % icru_numbers)
        # if ICRU references were found - get file names for them
        if icru_numbers:
            icru_file_names = self._decrypt_icru_files(icru_numbers)
            print(icru_file_names)

    @staticmethod
    def _parse_beam_file(file_path):
        """Scan BEAM.dat file for references to external files and return them"""
        external_files = []
        with open(file_path, 'r') as beam_f:
            for line in beam_f.readlines():
                _split_line = line.split()
                # line length checking to prevent IndexError
                if _split_line.__len__() > 0 and _split_line[0] == "USEBMOD":
                    logger.debug("Found reference to external file in BEAM file: {0} {1}".format(
                                 _split_line[0], _split_line[2]))
                    external_files.append(_split_line[2])
                elif _split_line.__len__() > 0 and _split_line[0] == "USECBEAM":
                    logger.debug("Found reference to external file in BEAM file: {0} {1}".format(
                        _split_line[0], _split_line[1]))
                    external_files.append(_split_line[1])
        return external_files

    @staticmethod
    def _parse_mat_file(file_path):
        """Scan MAT.dat file for ICRU references to files and return found ICRU numbers"""
        icru_numbers = []
        with open(file_path, 'r') as mat_f:
            for line in mat_f.readlines():
                _split_line = line.split()
                if _split_line.__len__() > 1 and _split_line[0] == "ICRU":
                    print(_split_line[1])
                    icru_numbers.append(_split_line[1])
        return icru_numbers

    def _decrypt_icru_files(self, numbers):
        """Find matching file names for given ICRU numbers"""
        # load ICRU reference file
        icru_file_path = os.path.join('mcengine', 'data', 'ICRU_table')
        with open(icru_file_path, 'r') as table_f:
            # first element of file is ICRU ID, second is file name it references
            ref_dict = {line.split()[0]: line.split()[1] for line in table_f.readlines()}
        return [ref_dict[e] for e in numbers]

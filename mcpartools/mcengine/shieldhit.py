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

    def find_external_files(self):
        """Scan all SHIELDHIT12A config files to find external files used and return it"""
        beam_file, geo_file, mat_file, _ = self.input_files
        # abs_output_dir = os.path.abspath(output_dir)
        external_beam_files = self._parse_beam_file(beam_file)
        logger.info("External files found in BEAM file: {0}".format(external_beam_files))
        icru_numbers = self._parse_mat_file(mat_file)
        logger.info("ICRU references found in MAT file: {0}".format(icru_numbers))
        # if ICRU references were found - get file names for material files
        icru_files = []
        if icru_numbers:
            icru_files = self._decrypt_icru_files(icru_numbers)
        geo_files = self._parse_geo_file(geo_file)
        logger.info("External files in GEO file: {0}".format(geo_file))
        external_files = external_beam_files + icru_files + geo_files
        return [os.path.join(self.input_path, e) for e in external_files]

    @staticmethod
    def _parse_beam_file(file_path):
        """Scan SH12A BEAM file for references to external files and return them"""
        external_files = []
        with open(file_path, 'r') as beam_f:
            for line in beam_f.readlines():
                split_line = line.split()
                # line length checking to prevent IndexError
                if len(split_line) > 2 and split_line[0] == "USEBMOD":
                    logger.debug("Found reference to external file in BEAM file: {0} {1}".format(
                                 split_line[0], split_line[2]))
                    external_files.append(split_line[2])
                elif len(split_line) > 1 and split_line[0] == "USECBEAM":
                    logger.debug("Found reference to external file in BEAM file: {0} {1}".format(
                                 split_line[0], split_line[1]))
                    external_files.append(split_line[1])
        return external_files

    def _parse_geo_file(self, file_path):
        """Scan SH12A GEO file for references to external files (like voxelised geometry) and return them"""
        external_files = []
        with open(file_path, 'r') as geo_f:
            for line in geo_f.readlines():
                split_line = line.split()
                if len(split_line) > 0:
                    base_path = os.path.join(self.input_path, split_line[0])
                    if os.path.isfile(base_path + '.hed'):
                        logger.debug("Found ctx + hed files: {0}".format(base_path))
                        external_files.append(base_path + '.hed')
                        if os.path.isfile(base_path + '.ctx'):
                            external_files.append(base_path + '.ctx')
                        elif os.path.isfile(base_path + '.ctx.gz'):
                            external_files.append(base_path + '.ctx.gz')
        return external_files

    @staticmethod
    def _parse_mat_file(file_path):
        """Scan SH12A MAT file for ICRU references to files and return found numbers"""
        icru_numbers = []
        with open(file_path, 'r') as mat_f:
            for line in mat_f.readlines():
                split_line = line.split()
                if len(split_line) > 1 and split_line[0] == "ICRU":
                    icru_numbers.append(split_line[1])
        return icru_numbers

    @staticmethod
    def _decrypt_icru_files(numbers):
        """Find matching file names for given ICRU numbers"""
        import json
        icru_file = resource_string(__name__, 'data/SH12A_ICRU_table.json')
        ref_dict = json.loads(icru_file.decode('utf-8'))
        return [ref_dict[e] for e in numbers]

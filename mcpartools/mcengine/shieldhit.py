import logging
import os
from pkg_resources import resource_string

from mcpartools.mcengine.mcengine import Engine

logger = logging.getLogger(__name__)


class ShieldHit(Engine):
    default_run_script_path = os.path.join('data', 'run_shieldhit.sh')
    regression_cfg_path = os.path.join('data', 'regression.ini')
    output_wildcard = "*.bdo"

    def __init__(self, input_path, mc_run_script, collect_method, mc_engine_options):
        Engine.__init__(self, input_path, mc_run_script, collect_method, mc_engine_options)

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

        self.config = self.regression_config
        if self.config is None:
            logger.warning("Could not properly parse configuration file for prediction feature")
        else:
            try:
                self.jobs_and_particles_regression = float(self.config["JOBS_AND_PARTICLES"])
                self.jobs_and_size_regression = [float(self.config["JOBS_AND_SIZE_A"]),
                                                 float(self.config["JOBS_AND_SIZE_B"])]
                self.files_and_size_regression = [float(self.config["FILES_AND_SIZE_A"]),
                                                  float(self.config["FILES_AND_SIZE_B"]),
                                                  float(self.config["FILES_AND_SIZE_C"])]
                self.density_and_size_regression = float(self.config["DENSITY_AND_SIZE"])
                self.collect_std_deviation = float(self.config['COLLECT_STANDARD_DEVIATION'])
                self.calculation_std_deviation = float(self.config['CALCULATION_STANDARD_DEVIATION'])
                self.max_predicted_job_number = float(self.config['MAX_JOB_NUMBER'])
                self.smallCollectFileCoef = float(self.config['SMALL_FILE_COEF'])
                self.min_collect_time = float(self.config['MIN_COLLECT_TIME'])
                self.mv_collect_time = float(self.config['MV_COLLECT_TIME'])
            except ValueError:
                logger.warning("Config file could not be read properly! Probably coefficients are not floats")
            except KeyError:
                logger.warning("Config file could not be read properly! Probably missing some variables")

        self.collect_script_content = resource_string(__name__, self.collect_script).decode('ascii')

        self.files_size = self.calculate_size()
        if self.files_size is not None:
            self.files_no_multiplier = 1 if self.files_size[0] == 0 else (
                self.files_size[1] / 10.0
            ) * self.files_and_size_regression[0] * (
                self.files_size[0] - self.files_and_size_regression[1]
            ) ** 2 + self.files_and_size_regression[2] * ((self.files_size[1] + 10) / 10.0)

        self.particle_no = 1
        self.rng_seed = 1

    def __str__(self):
        return "ShieldHit"

    @property
    def input_files(self):
        base = os.path.abspath(self.input_path)
        files = ('beam.dat', 'geo.dat', 'mat.dat', 'detect.dat')
        result = (os.path.join(base, f) for f in files)
        return result

    @property
    def regression_config(self):
        try:
            from configparser import ConfigParser
            config = ConfigParser()
            cfg_rs = resource_string(__name__, self.regression_cfg_path)
            config_string = cfg_rs.decode('ascii')
            config.read_string(config_string)
            if config.has_section("SHIELDHIT"):
                return config["SHIELDHIT"]
        except ImportError:
            logger.error("configparser not found. Please install configparser or avoid -P option")
        return None

    def randomize(self, new_seed, output_dir=None):
        self.rng_seed = new_seed

    def set_particle_no(self, particle_no):
        self.particle_no = particle_no

    def save_input(self, output_dir):
        logger.debug("input files are not modified, we will used shieldhit switches instead")

    def save_run_script(self, output_dir, job_id):
        beam_file, geo_file, mat_file, detect_file = self.input_files
        abs_output_dir = os.path.abspath(output_dir)
        # SH12A should use configs we copied/edited
        # go up from 'workspace/job_xxxx' to 'run_xxxxxxxx' dir and add 'input/'
        input_dir = os.path.abspath(os.path.join(abs_output_dir, '..', '..', 'input'))
        contents = self.run_script_content.format(
            shieldhit_bin='shieldhit',
            engine_options=self.engine_options,
            working_directory=abs_output_dir,
            particle_no=self.particle_no,
            rnd_seed=self.rng_seed,
            # append config file name to run dir input directory path
            beam_file=os.path.join(input_dir, os.path.basename(beam_file)),
            geo_file=os.path.join(input_dir, os.path.basename(geo_file)),
            mat_file=os.path.join(input_dir, os.path.basename(mat_file)),
            detect_file=os.path.join(input_dir, os.path.basename(detect_file))
        )
        out_file_name = "run.sh"
        out_file_path = os.path.join(output_dir, out_file_name)
        out_fd = open(out_file_path, 'w')
        out_fd.write(contents)
        out_fd.close()
        os.chmod(out_file_path, 0o750)

    def find_external_files(self, run_input_dir):
        """
        Scan all SHIELDHIT12A config files to find external files used and return them.
        Also change paths in config files to match convention that all resources are
        symlinked in job_xxxx/symlink
        """
        beam_file, geo_file, mat_file, _ = self.input_files

        # check for external files in BEAM input file
        external_beam_files = self._parse_beam_file(beam_file, run_input_dir)
        if external_beam_files:
            logger.info("External files from BEAM file: {0}".format(external_beam_files))
        else:
            logger.debug("No external files from BEAM file")

        # check for external files in MAT input file
        icru_numbers = self._parse_mat_file(mat_file)
        if icru_numbers:
            logger.info("External files from MAT file: {0}".format(icru_numbers))
        else:
            logger.debug("No external files from MAT file")
        # if ICRU+LOADEX pairs were found - get file names for external material files
        icru_files = []
        if icru_numbers:
            icru_files = self._decrypt_icru_files(icru_numbers)

        # check for external files in GEO input file
        geo_files = self._parse_geo_file(geo_file, run_input_dir)
        if geo_files:
            logger.info("External files from GEO file: {0}".format(geo_files))
        else:
            logger.debug("No external files from GEO file")

        external_files = external_beam_files + icru_files + geo_files
        return [os.path.join(self.input_path, e) for e in external_files]

    def _parse_beam_file(self, file_path, run_input_dir):
        """Scan SH12A BEAM file for references to external files and return them"""
        external_files = []
        paths_to_replace = []
        with open(file_path, 'r') as beam_f:
            for line in beam_f.readlines():
                split_line = line.split()
                # line length checking to prevent IndexError
                if len(split_line) > 2 and split_line[0] == "USEBMOD":
                    logger.debug("Found reference to external file in BEAM file: {0} {1}".format(
                        split_line[0], split_line[2]))
                    external_files.append(split_line[2])
                    paths_to_replace.append(split_line[2])
                elif len(split_line) > 1 and split_line[0] == "USECBEAM":
                    logger.debug("Found reference to external file in BEAM file: {0} {1}".format(
                        split_line[0], split_line[1]))
                    external_files.append(split_line[1])
                    paths_to_replace.append(split_line[1])
        if paths_to_replace:
            run_dir_config_file = os.path.join(run_input_dir, os.path.split(file_path)[-1])
            logger.debug("Calling rewrite_paths method on file: {0}".format(run_dir_config_file))
            self._rewrite_paths_in_file(run_dir_config_file, paths_to_replace)
        return external_files

    def _parse_geo_file(self, file_path, run_input_dir):
        """Scan SH12A GEO file for references to external files (like voxelised geometry) and return them"""
        external_files = []
        paths_to_replace = []
        with open(file_path, 'r') as geo_f:
            for line in geo_f.readlines():
                split_line = line.split()
                if len(split_line) > 0 and not line.startswith("*"):
                    base_path = os.path.join(self.input_path, split_line[0])
                    if os.path.isfile(base_path + '.hed'):
                        logger.debug("Found ctx + hed files: {0}".format(base_path))
                        external_files.append(base_path + '.hed')
                        # try to find ctx file
                        if os.path.isfile(base_path + '.ctx'):
                            external_files.append(base_path + '.ctx')
                        elif os.path.isfile(base_path + '.ctx.gz'):
                            external_files.append(base_path + '.ctx.gz')
                        # replace path to match symlink location
                        paths_to_replace.append(split_line[0])
        if paths_to_replace:
            run_dir_config_file = os.path.join(run_input_dir, os.path.split(file_path)[-1])
            logger.debug("Calling rewrite_paths method on file: {0}".format(run_dir_config_file))
            self._rewrite_paths_in_file(run_dir_config_file, paths_to_replace)
        return external_files

    def _parse_mat_file(self, file_path):
        """Scan SH12A MAT file for ICRU+LOADEX pairs and return found ICRU numbers"""
        mat_file_sections = self._extract_mat_sections(file_path)
        return self._analyse_mat_sections(mat_file_sections)

    @staticmethod
    def _extract_mat_sections(file_path):
        with open(file_path, 'r') as mat_f:
            chunks = []
            current_chunk = []
            for line in mat_f:
                if line.startswith("MEDIUM") and current_chunk:
                    # if line starts with MEDIUM - new section, add all gathered data to chunks
                    chunks.append(current_chunk[:])
                    current_chunk = []
                elif line.startswith("ICRU") or line.startswith("LOADDEDX"):
                    # if line contains ICRU or LOADDEDX add it to current section chunk
                    current_chunk.append(line.strip())
            chunks.append(current_chunk)  # append the last chunk outside the loop
        return chunks

    @staticmethod
    def _analyse_mat_sections(sections):
        """
        Cases:
        - ICRU flag present, LOADDEDX flag missing -> data loaded from some data hardcoded in SH12A binary,
        no need to load external files
        - ICRU flag present, LOADDEDX flag present -> data loaded from external files. ICRU number read from ICRU flag,
        any number following LOADDEDX flag is ignored.
        - ICRU flag missing, LOADDEDX flag present -> data loaded from external files. ICRU number read from LOADDEDX
        - ICRU flag missing, LOADDEDX flag missing -> nothing happens
        """
        icru_numbers = []
        for section in sections:
            load_present = False
            load_value = False
            icru_value = False
            for e in section:
                split_line = e.split()
                if "LOADDEDX" in e:
                    load_present = True
                    if len(split_line) > 1:
                        load_value = split_line[1] if "!" not in split_line[1] else False  # ignore ! comments
                elif "ICRU" in e and len(split_line) > 1:
                    icru_value = split_line[1] if "!" not in split_line[1] else False  # ignore ! comments
            if load_present:  # LOADDEDX is present, so external file is required
                if icru_value:  # if ICRU value was given
                    icru_numbers.append(icru_value)
                elif load_value:  # if only LOADDEDX with values was present in section
                    icru_numbers.append(load_value)
        return icru_numbers

    @staticmethod
    def _decrypt_icru_files(numbers):
        """Find matching file names for given ICRU numbers"""
        import json
        icru_file = resource_string(__name__, os.path.join('data', 'SH12A_ICRU_table.json'))
        ref_dict = json.loads(icru_file.decode('ascii'))
        try:
            return [ref_dict[e] for e in numbers]
        except KeyError as er:
            logger.error("There is no ICRU file for id: {0}".format(er))
            raise

    @staticmethod
    def _rewrite_paths_in_file(config_file, paths_to_replace):
        """
        Rewrite paths in config files to match convention job_xxxx/symlink
        Requires path to run_xxxx/input/config_file and a list of paths_to_replace
        """
        lines = []
        # make a copy of config
        import shutil
        shutil.copyfile(config_file, str(config_file + '_original'))
        with open(config_file) as infile:
            for line in infile:
                for old_path in paths_to_replace:
                    if old_path in line:
                        new_path = os.path.split(old_path)[-1]
                        line = line.replace(old_path, new_path)
                        logger.debug("Changed path {0} ---> {1} in file {2}".format(old_path, new_path, config_file))
                lines.append(line)
        with open(config_file, 'w') as outfile:
            for line in lines:
                outfile.write(line)

    def predict_best(self, total_particle_no, collect_type):
        try:
            import numpy as np
            # This type of collect almost not affect calculation time
            if collect_type == "mv":
                return self.max_predicted_job_number

            # The coefficients correspond to the derivative function. That function was found experimentally
            # For small output file, collect behave differently than for big ones
            elif self.files_size[0] < 10:
                coeff = [
                    self.collect_std_deviation * self.files_no_multiplier * self.collect_coefficient(
                        collect_type
                    ) * 3 * self.smallCollectFileCoef, 0, 0, 0,
                    - self.jobs_and_particles_regression * total_particle_no * self.calculation_std_deviation
                ]
            else:
                coeff = [
                    self.collect_std_deviation * self.files_no_multiplier * self.collect_coefficient(collect_type) *
                    (self.jobs_and_size_regression[1] * self.files_size[0] ** 2 +
                     self.jobs_and_size_regression[0] * self.files_size[0]), 0,
                    - self.jobs_and_particles_regression * total_particle_no * self.calculation_std_deviation
                ]

            # smallest, real solution
            results = [int(x.real) for x in np.roots(coeff) if np.isreal(x) and x.real > 0]
            result = sorted([(x, self._calculation_time(total_particle_no, x, collect_type)) for x in results],
                            key=lambda x: x[1])[0][0]

            result = self.max_predicted_job_number if result > self.max_predicted_job_number else result
            return result
        except ZeroDivisionError:
            # output file is extremely small
            result = self.max_predicted_job_number
        except AttributeError:
            logger.error("Could not predict configuration! Check correctness of config file for prediction feature")
        except ImportError as e:
            logger.error("Numpy not found. Please install numpy or avoid -P option")
            raise e
        return None

    def calculate_size(self):
        try:
            beam_file, geo_file, mat_file, detect_file = self.input_files
            count = True
            a = self.density_and_size_regression
            files_size = 0
            i = 0
            counter = 0
            with open(detect_file, 'r') as detect:  # calculate sizes and number of entries
                for line in detect:
                    if line[0] == "*":  # new entry in detect.dat
                        i = 0
                    if i % 4 == 1:  # check if this entry is GEOMAP and if so, do not take it into account
                        count = True
                        scoring = line.split()[0]
                        logger.debug("Found {0} in detect.dat".format(scoring))
                        if scoring == "GEOMAP":
                            count = False
                    if i % 4 == 2 and count:  # Calculate size of entry and increment counter
                        x, y, z = [int(j) for j in line.split()[0:3]]
                        files_size += a * (x * y * z) / 1000000
                        counter += 1
                        logger.debug("x = {0}, y = {1}, z = {2}, files_size = {3} ".format(x, y, z, files_size))
                    i += 1
            return files_size, counter
        except AttributeError:
            logger.error("Could not calculate size of files! Check correctness of config file for prediction feature")
            return None

    def calculation_time(self, particles_no_per_job, jobs_no, collect_type):
        return self._calculation_time(particles_no_per_job * jobs_no, jobs_no, collect_type)

    def _calculation_time(self, total_particles_no, jobs_no, collect_type):
        try:
            # This type of collect has constant execution time
            if collect_type == "mv":
                collect_time = self.mv_collect_time
            elif self.files_size[0] < 10:
                collect_time = self.min_collect_time + self.smallCollectFileCoef * (jobs_no ** 3)
            else:
                collect_time = (
                    self.jobs_and_size_regression[0] * self.files_size[0] * jobs_no +
                    self.jobs_and_size_regression[1] * jobs_no * self.files_size[0] ** 2
                )

            calc_time = self.jobs_and_particles_regression * (1 / float(jobs_no)) * total_particles_no
            collect_time *= self.files_no_multiplier * self.collect_std_deviation
            collect_coef = self.collect_coefficient(collect_type)
            if collect_coef > 0:
                collect_time *= collect_coef

            calc_time *= self.calculation_std_deviation

            return collect_time + calc_time
        except AttributeError:
            logger.error("Could not estimate calculation time! Check correctness of config file for prediction feature")
            return None

    def collect_coefficient(self, collect_option):
        collect_coef = {
            'mv': self.config['MV_COLLECT_COEF'],
            'cp': self.config['CP_COLLECT_COEF'],
            'plotdata': self.config['PLOTDATA_COLLECT_COEF'],
            'image': self.config['IMAGE_COLLECT_COEF'],
            'custom': self.config['CUSTOM_COLLECT_COEF'],
        }[collect_option]

        return float(collect_coef)

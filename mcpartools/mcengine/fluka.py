import logging
import os
from pkg_resources import resource_string

from mcpartools.mcengine.mcengine import Engine

logger = logging.getLogger(__name__)


class Fluka(Engine):

    collect_script = os.path.join('data', 'collect_fluka.sh')

    default_run_script_path = os.path.join('data', 'run_fluka.sh')

    def __init__(self, input_path, mc_run_script):
        Engine.__init__(self, input_path, mc_run_script)

        # user didn't provided path to input scripts, use default
        if self.run_script_path is None:
            tpl = resource_string(__name__, self.default_run_script_path)
            self.run_script_content = tpl.decode('ascii')
            logger.debug("Using default run script: " +
                         self.default_run_script_path)
        else:
            tpl_fd = open(self.run_script_path, 'r')
            self.run_script_content = tpl_fd.read()
            tpl_fd.close()
            logger.debug("Using user run script: " + self.run_script_path)
        in_file = self.input_path
        in_fd = open(in_file, 'r')
        self.input_lines = in_fd.readlines()
        in_fd.close()

        self.collect_script_content = resource_string(
            __name__, self.collect_script).decode('ascii')

    @property
    def input_files(self):
        # TODO check if additional files are needed
        result = [self.input_path]
        logger.debug("Input files: " + ",".join(result))
        return result

    def randomize(self, new_seed):
        result = []
        # TODO think of using flair API for that purpose
        for l in self.input_lines:
            # TODO better discovery needed
            if l.startswith("RANDOMIZ"):
                # TODO check formatting
                new_line = "RANDOMIZ         1.0 {:f}\n".format(new_seed)
                logger.debug("Replace RAND line with [" + new_line[:-1] + "]")
                result.append(new_line)
            else:
                result.append(l)
        self.input_lines = result

    def set_particle_no(self, particle_no):
        result = []
        for l in self.input_lines:
            # TODO better discovery needed
            if l.startswith("START"):
                # TODO check formatting
                new_line = "START        {:10.1f}\n".format(particle_no)
                result.append(new_line)
                logger.debug("Replace START line with [" + new_line[:-1] + "]")
            else:
                result.append(l)
        self.input_lines = result

    def save_input(self, output_dir):
        out_file_name = os.path.basename(self.input_path)
        out_file_path = os.path.join(output_dir, out_file_name)
        out_fd = open(out_file_path, 'w')
        for l in self.input_lines:
            out_fd.write(l)
        out_fd.close()

    def save_run_script(self, output_dir, jobid):
        input_base_name = os.path.basename(self.input_path)[:-4]
        output_dir_abs_path = os.path.abspath(output_dir)
        contents = self.run_script_content.format(
            working_directory=output_dir_abs_path,
            input_basename=input_base_name,
            job_id=jobid)
        out_file_name = "run.sh"
        out_file_path = os.path.join(output_dir, out_file_name)
        out_fd = open(out_file_path, 'w')
        out_fd.write(contents)
        out_fd.close()
        os.chmod(out_file_path, 0o750)

    def write_collect_script(self, output_dir):
        output_dir_abs_path = os.path.abspath(output_dir)
        contents = self.collect_script_content.format(
            output_dir=output_dir_abs_path)
        out_file_name = "collect.sh"
        out_file_path = os.path.join(output_dir, out_file_name)
        out_fd = open(out_file_path, 'w')
        out_fd.write(contents)
        out_fd.close()
        os.chmod(out_file_path, 0o750)

import logging
import os

from mcpartools.mcengine.mcengine import Engine

logger = logging.getLogger(__name__)


class Fluka(Engine):

    run_script = """#!/bin/bash
# go to working directory
cd {:s}
# run rfluka
rfluka -N{:d} -M{:d} {:s}
"""

    collect_script = """#!/bin/bash
cp XXX YYY {:s}
"""

    def __init__(self, input_path, mc_run_script):
        super().__init__(input_path, mc_run_script)
        if self.run_script is None:
            self.run_script = Fluka.run_script
        in_file = self.input_path
        in_fd = open(in_file, 'r')
        self.input_lines = in_fd.readlines()
        in_fd.close()

    @property
    def input_files(self):
        # TODO check if additional files are needed
        result = [self.input_path]
        logger.debug("Input files: " + ",".join(result))
        return result

    def randomize(self, new_seed):
        result = []
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
        contents = self.run_script.format(output_dir, jobid,
                                          jobid + 1, input_base_name)
        out_file_name = "run.sh"
        out_file_path = os.path.join(output_dir, out_file_name)
        out_fd = open(out_file_path, 'w')
        out_fd.write(contents)
        out_fd.close()

    def write_collect_script(self, output_dir):
        contents = self.collect_script.format(output_dir)
        out_file_name = "collect.sh"
        out_file_path = os.path.join(output_dir, out_file_name)
        out_fd = open(out_file_path, 'w')
        out_fd.write(contents)
        out_fd.close()

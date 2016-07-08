import os

from mcpartools.mcengine.mcengine import Engine


class ShieldHit(Engine):

    run_script = """#!/bin/bash
shieldhit .... {:s}
"""

    @property
    def input_files(self):
        base = self.input_path
        # TODO add *.txt files with stopping power
        # TODO add *.ctx/.hed files with CT scans
        files = ['beam.dat', 'geo.dat', 'mat.dat', 'detect.dat']
        result = [os.path.join(base, f) for f in files]
        return result

    def randomize(self, output_dir, new_seed):
        pass

    def set_particle_no(self, particle_no):
        "in memory"
        pass

    def save_input(self, output_dir):
        "nothing, we will use switches -b, -g etc"
        pass

    def save_run_script(self, output_dir):
        contents = self.run_script.format(output_dir)
        out_file_name = "run.sh"
        out_file_path = os.path.join(output_dir, out_file_name)
        out_fd = open(out_file_path, 'w')
        out_fd.write(contents)
        out_fd.close()

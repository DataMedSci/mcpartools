import os
import tempfile
import unittest

import shutil

from mcpartools import generatemc


class TestRunGenerate(unittest.TestCase):

    def setUp(self):
        self.main_dir = os.path.join("tests", "res")

    def test_help(self):
        try:
            generatemc.main(["--help"])
        except SystemExit as e:
            self.assertEqual(e.code, 0)

    def test_version(self):
        try:
            generatemc.main(["--version"])
        except SystemExit as e:
            self.assertEqual(e.code, 0)

    def test_slurm_fluka_input_ok(self):
        working_dir = tempfile.mkdtemp()  # make temp working dir
        fluka_input = os.path.join(self.main_dir, "sample_fluka.inp")
        ret_code = generatemc.main(["-j", "2", "-p", "100", "-w", working_dir, "-b", "slurm", fluka_input])
        self.assertEqual(ret_code, 0)
        shutil.rmtree(working_dir)

    def test_slurm_shieldhit_input_ok(self):
        working_dir = tempfile.mkdtemp()  # make temp working dir
        shieldhit_input = os.path.join(self.main_dir, "shieldhit")
        ret_code = generatemc.main(["-j", "2", "-p", "100", "-w", working_dir, "-b", "slurm", shieldhit_input])
        self.assertEqual(ret_code, 0)
        shutil.rmtree(working_dir)

    def test_slurm_shieldhit_scheduler_options(self):
        working_dir = tempfile.mkdtemp()  # make temp working dir
        shieldhit_input = os.path.join(self.main_dir, "shieldhit")
        ret_code = generatemc.main(["-j", "2", "-p", "100", "-w", working_dir, "-b", "slurm", "-s",
                                    "[--nodes=1 --ntasks-per-node=1 --mem=2000 --time=0:30:00]",
                                    shieldhit_input])
        self.assertEqual(ret_code, 0)
        shutil.rmtree(working_dir)

    def test_torque_fluka_input_ok(self):
        working_dir = tempfile.mkdtemp()  # make temp working dir
        fluka_input = os.path.join(self.main_dir, "sample_fluka.inp")
        ret_code = generatemc.main(["-j", "2", "-p", "100", "-w", working_dir, "-b", "torque", fluka_input])
        self.assertEqual(ret_code, 0)
        shutil.rmtree(working_dir)

    def test_torque_shieldhit_input_ok(self):
        working_dir = tempfile.mkdtemp()  # make temp working dir
        shieldhit_input = os.path.join(self.main_dir, "shieldhit")
        ret_code = generatemc.main(["-j", "2", "-p", "100", "-w", working_dir, "-b", "torque", shieldhit_input])
        self.assertEqual(ret_code, 0)
        shutil.rmtree(working_dir)

    def test_input_bad(self):
        try:
            generatemc.main(["-j", "2"])
        except SystemExit as e:
            self.assertEqual(e.code, 2)


if __name__ == '__main__':
    unittest.main()

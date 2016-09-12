import os
import time
import unittest

from mcpartools import generatemc


class TestRunGenerate(unittest.TestCase):

    def setUp(self):
        self.main_dir = os.path.join("tests", "res")

    def test_help(self):
        time.sleep(1)  # TODO should be removed after fixing https://github.com/DataMedSci/mcpartools/issues/14
        try:
            generatemc.main(["--help"])
        except SystemExit as e:
            self.assertEqual(e.code, 0)

    def test_version(self):
        time.sleep(1)
        try:
            generatemc.main(["--version"])
        except SystemExit as e:
            self.assertEqual(e.code, 0)

    def test_fluka_input_ok(self):
        time.sleep(1)
        fluka_input = os.path.join(self.main_dir, "sample_fluka.inp")
        ret_code = generatemc.main(["-j", "2", "-p", "100", fluka_input])
        self.assertEqual(ret_code, 0)

    def test_shieldhit_input_ok(self):
        time.sleep(1)
        shieldhit_input = os.path.join(self.main_dir, "shieldhit")
        ret_code = generatemc.main(["-j", "2", "-p", "100", shieldhit_input])
        self.assertEqual(ret_code, 0)

    def test_shieldhit_scheduler_options(self):
        time.sleep(1)
        shieldhit_input = os.path.join(self.main_dir, "shieldhit")
        ret_code = generatemc.main(["-j", "2", "-p", "100", "-s",
                                    "--nodes=1 --ntasks-per-node=1 --mem=2000 --time=0:30:00",
                                    shieldhit_input])
        self.assertEqual(ret_code, 0)

    def test_input_bad(self):
        time.sleep(1)
        try:
            generatemc.main(["-j", "2"])
        except SystemExit as e:
            self.assertEqual(e.code, 2)

if __name__ == '__main__':
    unittest.main()

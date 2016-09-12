import os
import unittest

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

    def test_fluka_input_ok(self):
        fluka_input = os.path.join(self.main_dir, "sample_fluka.inp")
        ret_code = generatemc.main(["-j", "2", "-p", "100", fluka_input])
        self.assertEqual(ret_code, 0)

    def test_shieldhit_input_ok(self):
        shieldhit_input = os.path.join(self.main_dir, "shieldhit")
        ret_code = generatemc.main(["-j", "2", "-p", "100", shieldhit_input])
        self.assertEqual(ret_code, 0)

    def test_input_bad(self):
        try:
            generatemc.main(["-j", "2"])
        except SystemExit as e:
            self.assertEqual(e.code, 2)

if __name__ == '__main__':
    unittest.main()

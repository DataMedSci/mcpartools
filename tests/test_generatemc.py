import unittest

from mcpartools import generatemc


class TestFunMethod(unittest.TestCase):
    def test_help(self):
        self.assertRaises(SystemExit, generatemc.main, ["--help"])

    def test_version(self):
        self.assertRaises(SystemExit, generatemc.main, ["--version"])

    def test_input(self):
        self.assertRaises(SystemExit, generatemc.main, ["."])


if __name__ == '__main__':
    unittest.main()

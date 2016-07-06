import unittest

from mcpartools import generatemc


class TestFunMethod(unittest.TestCase):
    def test_check(self):
        generatemc.main()
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()

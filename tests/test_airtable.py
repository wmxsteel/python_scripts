# Created by alanhu at 8/31/23
import unittest
import sys
import os
from pathlib import Path

# Get the directory of the current script
current_script_directory = os.path.dirname(os.path.abspath(__file__))

# Get the parent directory
parent_directory = os.path.dirname(current_script_directory)

# Append the parent directory to sys.path
sys.path.append(parent_directory)


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, False)  # add assertion here


if __name__ == '__main__':
    unittest.main()

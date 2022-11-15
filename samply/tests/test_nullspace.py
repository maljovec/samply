""" This module will test the functionality of samply.nullspace
"""
import unittest

import numpy as np

import samply


class TestNullspace(unittest.TestCase):
    """Class for testing the nullspace function"""

    def setup(self):
        """ """
        pass

    def test_nullspace(self):
        """ """
        self.setup()
        A = np.array([[1, 0, 0], [0, 1, 0]])
        ns = samply.nullspace(A)
        zero = np.max(np.fabs(np.dot(A, ns)))
        self.assertLessEqual(zero, 1e-15)


if __name__ == "__main__":
    unittest.main()

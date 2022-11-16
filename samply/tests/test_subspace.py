""" This module will test the functionality of samply.SubspaceSampler
"""
import math
import unittest

import numpy as np

import samply


class TestSubspaceSampler(unittest.TestCase):
    """Class for testing the Subspace sampler"""

    def setup(self):
        """ """
        pass

    def test_invalid(self):
        """ """
        try:
            samply.subspace.orthogonal_ball([1], 1)
            self.assertEqual(True, False, "A ValueError should be raised.")
        except ValueError as err:
            self.assertEqual("Could not construct valid subspace.", str(err))

    def test_2D_x(self):
        """ """
        samples = samply.subspace.orthogonal_ball([1, 0], 1000)
        zero = np.unique(samples[:, 0])
        msg = "Samples drawn orthogonal to x-axis should have x=0"
        self.assertEqual(zero[0], 0, msg)

        samples = samply.subspace.orthogonal_directional([1, 0], 100)
        zero = np.unique(samples[:, 0])
        msg = "Samples drawn orthogonal to x-axis should have x=0"
        self.assertEqual(zero[0], 0, msg)
        msg = "There are only 2 directions orthogonal to (1,0)"
        self.assertEqual(len(samples), 2, msg)
        self.assertEqual(samples[0, 1], -1)
        self.assertEqual(samples[1, 1], 1)

    def test_2D_y(self):
        """ """
        samples = samply.subspace.orthogonal_directional([0, 1], 1000)
        zero = np.unique(samples[:, 1])
        msg = "Samples drawn orthogonal to y-axis should have y=0"
        self.assertEqual(zero[0], 0, msg)
        msg = "There are only 2 directions orthogonal to (0,1)"
        self.assertEqual(len(samples), 2, msg)
        self.assertEqual(samples[0, 0], 1)
        self.assertEqual(samples[1, 0], -1)

    def test_grassmannian(self):
        self.setup()
        samples = samply.subspace.grassmannian(10, 3, 2)

        for basis in samples:
            zero = math.fabs(basis[:, 0].dot(basis[:, 1]))
            msg = "Basis is not orthogonal"
            self.assertLessEqual(zero, 1e-15, msg)


if __name__ == "__main__":
    unittest.main()

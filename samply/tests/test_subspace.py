""" This module will test the functionality of samply.SubspaceSampler
"""
import unittest
import samply
import numpy as np


class TestSubspaceSampler(unittest.TestCase):
    """ Class for testing the Subspace sampler
    """

    def setup(self):
        """
        """
        pass

    def test_invalid(self):
        """
        """
        try:
            sampler = samply.SubspaceSampler([1])
            self.assertEqual(True, False, "A ValueError should be raised.")
        except ValueError as err:
            self.assertEqual(
                "Could not construct valid subspace.", str(err))

    def test_2D_x(self):
        """
        """
        sampler = samply.SubspaceSampler([1, 0])
        samples = sampler.generate_samples(1000)
        zero = np.unique(samples[:, 0])
        msg = "Samples drawn orthogonal to x-axis should have x=0"
        self.assertEqual(zero[0], 0, msg)
        samples = sampler.generate_ball_samples(10)
        zero = np.unique(samples[:, 0])
        msg = "Samples drawn orthogonal to x-axis should have x=0"
        self.assertEqual(zero[0], 0, msg)
        samples = sampler.generate_directional_samples(100)
        zero = np.unique(samples[:, 0])
        msg = "Samples drawn orthogonal to x-axis should have x=0"
        self.assertEqual(zero[0], 0, msg)
        msg = "There are only 2 directions orthogonal to (1,0)"
        self.assertEqual(len(samples), 2, msg)
        self.assertEqual(samples[0, 1], -1)
        self.assertEqual(samples[1, 1], 1)

    def test_2D_y(self):
        """
        """
        sampler = samply.SubspaceSampler([0, 1])
        samples = sampler.generate_samples(1000)
        zero = np.unique(samples[:, 1])
        msg = "Samples drawn orthogonal to y-axis should have y=0"
        self.assertEqual(zero[0], 0, msg)
        samples = sampler.generate_ball_samples(10)
        zero = np.unique(samples[:, 1])
        msg = "Samples drawn orthogonal to y-axis should have y=0"
        self.assertEqual(zero[0], 0, msg)
        samples = sampler.generate_directional_samples(100)
        zero = np.unique(samples[:, 1])
        msg = "Samples drawn orthogonal to y-axis should have y=0"
        self.assertEqual(zero[0], 0, msg)
        msg = "There are only 2 directions orthogonal to (0,1)"
        self.assertEqual(len(samples), 2, msg)
        self.assertEqual(samples[0, 0], 1)
        self.assertEqual(samples[1, 0], -1)


if __name__ == "__main__":
    unittest.main()

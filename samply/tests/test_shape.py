""" This module will test the functionality of samply.BallSampler
"""
import unittest

import numpy as np

import samply


class TestHypercubeSampler(unittest.TestCase):
    """Class for testing the Ball sampler"""

    def setup(self):
        """ """
        self.tolerance = 1e-1
        self.N = 10
        self.D = 2

    def test_concentric_shells(self):
        """ """
        self.setup()
        samples = samply.shape.concentric_shells(self.N, self.D)
        self.assertEqual(self.N, samples.shape[0])
        self.assertEqual(self.D, samples.shape[1])
        self.assertGreaterEqual(np.min(samples), 0)
        self.assertLessEqual(np.max(samples), 1)

    def test_cross(self):
        """ """
        self.setup()
        samples = samply.shape.cross(self.N, self.D)
        self.assertEqual(self.N, samples.shape[0])
        self.assertEqual(self.D, samples.shape[1])
        self.assertGreaterEqual(np.min(samples), 0)
        self.assertLessEqual(np.max(samples), 1)

    def test_curve(self):
        """ """
        self.setup()
        samples = samply.shape.curve(self.N, self.D)
        self.assertEqual(self.N, samples.shape[0])
        self.assertEqual(self.D, samples.shape[1])
        self.assertGreaterEqual(np.min(samples), 0)
        self.assertLessEqual(np.max(samples), 1)

    def test_shell(self):
        """ """
        self.setup()
        samples = samply.shape.shell(self.N, self.D)
        self.assertEqual(self.N, samples.shape[0])
        self.assertEqual(self.D, samples.shape[1])
        self.assertGreaterEqual(np.min(samples), 0)
        self.assertLessEqual(np.max(samples), 1)

    def test_stripes(self):
        """ """
        self.setup()
        samples = samply.shape.stripes(self.N, self.D)
        self.assertEqual(self.N, samples.shape[0])
        self.assertEqual(self.D, samples.shape[1])
        self.assertGreaterEqual(np.min(samples), 0)
        self.assertLessEqual(np.max(samples), 1)


if __name__ == "__main__":
    unittest.main()

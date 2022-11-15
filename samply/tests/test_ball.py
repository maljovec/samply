""" This module will test the functionality of samply.BallSampler
"""
import math
import unittest

import numpy as np
from scipy.stats import kstest, uniform

import samply


class TestBallSampler(unittest.TestCase):
    """Class for testing the Ball sampler"""

    def setup(self):
        """ """
        self.tolerance = 1e-1

    def test_2D_uniform(self):
        """ """
        np.random.seed(0)
        samples = samply.ball.uniform(10000, 2)
        norms = np.linalg.norm(samples, axis=1)
        msg = "At least one sample lies outside of the unit ball"
        self.assertLessEqual(np.max(norms), 1, msg)

        thetas = np.arctan2(samples[:, 1], samples[:, 0])
        thetas /= 2 * math.pi
        thetas += 0.5
        p = kstest(thetas, uniform.cdf)[1]
        msg = "The angles are not representative of a uniform distribution ({})".format(
            p
        )
        self.assertGreaterEqual(p, 0.05, msg)


if __name__ == "__main__":
    unittest.main()

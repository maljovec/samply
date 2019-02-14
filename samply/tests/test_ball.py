""" This module will test the functionality of samply.BallSampler
"""
import unittest
import samply
from scipy.stats import kstest, uniform
import numpy as np
import math

class TestBallSampler(unittest.TestCase):
    """ Class for testing the Ball sampler
    """

    def setup(self):
        """
        """
        pass

    def test_2D(self):
        """
        """
        ball_sampler = samply.BallSampler(2)
        np.random.seed(0)
        samples = ball_sampler.generate_samples(10000)
        norms = np.linalg.norm(samples, axis=1)
        msg = "At least one sample lies outside of the unit ball"
        self.assertLessEqual(np.max(norms), 1, msg)

        thetas = np.arctan2(samples[:, 1], samples[:, 0])
        thetas /= 2*math.pi
        thetas += 0.5
        p = kstest(thetas, uniform.cdf)[1]
        msg = "The angles are not representative of a uniform distribution ({})".format(p)
        self.assertGreaterEqual(p, 0.05, msg)

if __name__ == "__main__":
    unittest.main()
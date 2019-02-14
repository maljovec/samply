""" This module will test the functionality of samply.GrassmannianSampler
"""
import unittest
import samply
import numpy as np
import math


class TestGrassmannianSampler(unittest.TestCase):
    """ Class for testing the Grassmannian sampler
    """

    def setup(self):
        """
        """
        pass

    def test_case(self):
        self.setup()
        sampler = samply.GrassmannianSampler(3, 2)
        samples = sampler.generate_samples(10)

        for basis in samples:
            zero = math.fabs(basis[:, 0].dot(basis[:, 1]))
            msg = "Basis is not orthogonal"
            self.assertLessEqual(zero, 1e-15, msg)


if __name__ == "__main__":
    unittest.main()

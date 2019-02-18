""" This module will test the functionality of samply.BallSampler
"""
import unittest
import samply
from scipy.stats import kstest, uniform
from sklearn import neighbors
import numpy as np
import math


class TestHypercubeSampler(unittest.TestCase):
    """ Class for testing the Ball sampler
    """

    def setup(self):
        """
        """
        self.tolerance = 1e-1

    def n_dimension_cvt_validation(self, n_samples, n_validation, D):
        points = samply.hypercube.cvt(n_samples, D, verbose=True)
        query_points = samply.hypercube.uniform(n_validation, D)
        nn = neighbors.NearestNeighbors(n_neighbors=1)
        nn.fit(points)
        sites = nn.kneighbors(query_points, return_distance=False)
        N = points.shape[0]
        D = points.shape[1]

        counts = np.zeros(N)
        coms = np.zeros((N, D))
        for i, pt in zip(sites, query_points):
            counts[i] += 1
            coms[i] += pt

        coms /= counts[:, None]
        max_error = np.max(np.linalg.norm(points - coms, axis=1))
        self.assertLessEqual(
            max_error,
            self.tolerance,
            "Error ({}) exceeds tolerance {}".format(max_error, self.tolerance),
        )

    def test_2D_cvt_small(self):
        """
        """
        self.setup()
        np.random.seed(0)
        self.n_dimension_cvt_validation(10, 100000, 2)


if __name__ == "__main__":
    unittest.main()

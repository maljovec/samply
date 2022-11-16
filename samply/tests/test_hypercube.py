""" This module will test the functionality of samply.BallSampler
"""
import unittest

import numpy as np
from sklearn import neighbors

import samply


class TestHypercubeSampler(unittest.TestCase):
    """Class for testing the Ball sampler"""

    def setup(self):
        """ """
        self.tolerance = 1e-1

    def n_dimension_cvt_validation(self, n_samples, n_validation, D):
        points = samply.hypercube.cvt(n_samples, D, verbose=False)
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

    def test_cvt_verbosity(self):
        """ """
        samples = samply.hypercube.cvt(10, 2, verbose=True)
        self.assertEqual(10, samples.shape[0])
        self.assertEqual(2, samples.shape[1])

    def test_2D_cvt_small(self):
        """ """
        self.setup()
        np.random.seed(0)
        self.n_dimension_cvt_validation(10, 100000, 2)

    def test_2D_cvt_moderate(self):
        """ """
        self.setup()
        np.random.seed(0)
        self.n_dimension_cvt_validation(1000, 100000, 2)

    def test_3D_cvt_moderate(self):
        """ """
        self.setup()
        np.random.seed(0)
        self.n_dimension_cvt_validation(1000, 100000, 3)

    def test_lhs(self):
        """ """
        self.setup()
        np.random.seed(0)
        samples = samply.hypercube.lhs(10, 2)
        self.assertEqual(10, samples.shape[0])
        self.assertEqual(2, samples.shape[1])
        self.assertGreaterEqual(np.min(samples), 0)
        self.assertLessEqual(np.max(samples), 1)

    def test_halton(self):
        """ """
        self.setup()
        np.random.seed(0)
        samples = samply.hypercube.halton(10, 2)
        self.assertEqual(10, samples.shape[0])
        self.assertEqual(2, samples.shape[1])
        self.assertGreaterEqual(np.min(samples), 0)
        self.assertLessEqual(np.max(samples), 1)

    def test_grid(self):
        """ """
        self.setup()
        D = 2
        N = 10**D
        samples = samply.hypercube.grid(N, D)
        self.assertEqual(N, samples.shape[0])
        self.assertEqual(D, samples.shape[1])
        for i in range(D):
            self.assertEqual(samples[0, i], 0.0)
            self.assertEqual(samples[-1, i], 1.0)
        self.assertGreaterEqual(np.min(samples), 0)
        self.assertLessEqual(np.max(samples), 1)

    def test_normal(self):
        """ """
        self.setup()
        N = 100000
        D = 2
        np.random.seed(0)
        samples = samply.hypercube.normal(N, D)
        self.assertEqual(N, samples.shape[0])
        self.assertEqual(D, samples.shape[1])
        self.assertGreaterEqual(np.min(samples), 0)
        self.assertLessEqual(np.max(samples), 1)
        means = np.fabs(np.mean(samples, axis=0) - 0.5)
        stds = np.fabs(np.std(samples, axis=0) - 0.15)
        for mu, sigma in zip(means, stds):
            self.assertLessEqual(mu, 1e-3)
            self.assertLessEqual(sigma, 1e-3)

    def test_multimodal(self):
        """ """
        self.setup()
        np.random.seed(0)
        samples = samply.hypercube.multimodal(10, 2)
        self.assertEqual(10, samples.shape[0])
        self.assertEqual(2, samples.shape[1])
        self.assertGreaterEqual(np.min(samples), 0)
        self.assertLessEqual(np.max(samples), 1)


if __name__ == "__main__":
    unittest.main()

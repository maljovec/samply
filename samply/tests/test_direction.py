""" This module will test the functionality of samply.DirectionalSampler
"""
import math
import unittest

import numpy as np
from scipy.stats import kstest, uniform
from sklearn import neighbors

import samply


class TestDirectionalSampler(unittest.TestCase):
    """Class for testing the Directional sampler"""

    def setup(self):
        """ """
        self.tolerance = 1e-1

    def test_1D_uniform(self):
        """ """
        samples = samply.directional.uniform(10000, 1)
        msg = "There should only be 2 samples available for the 1D case."
        self.assertEqual(len(samples), 2, msg)
        self.assertEqual(samples[0, 0], -1)
        self.assertEqual(samples[1, 0], 1)

    def test_2D_uniform(self):
        """ """
        samples = samply.directional.uniform(10000, 2)
        norms = np.linalg.norm(samples, axis=1)
        deltas = np.fabs(norms - 1.0)
        msg = "At least one sample does not represent a unit vector"
        self.assertLessEqual(np.max(deltas), 1e-6, msg)

        thetas = np.arctan2(samples[:, 1], samples[:, 0])
        thetas /= 2 * math.pi
        thetas += 0.5
        p = kstest(thetas, uniform.cdf)[1]
        msg = (
            "The angles are not representative of a uniform distribution (p={})".format(
                p
            )
        )
        self.assertGreaterEqual(p, 0.05, msg)

    def test_2D_cvt(self):
        """ """
        self.setup()
        n_samples = 20
        n_validation = 100000
        D = 2
        points = samply.directional.cvt(n_samples, D, verbose=True)
        deltas = np.fabs(np.linalg.norm(points, axis=1) - 1)
        msg = "A generated point does not lie on the sphere"
        self.assertLessEqual(np.max(deltas), 1e-6, msg)
        query_points = samply.ball.uniform(n_validation, D)

        nn = neighbors.NearestNeighbors(n_neighbors=1)
        nn.fit(points)
        sites = nn.kneighbors(query_points, return_distance=False)

        counts = np.zeros(n_samples)
        coms = np.zeros((n_samples, D))
        for i, pt in zip(sites, query_points):
            counts[i] += 1
            coms[i] += pt

        coms /= counts[:, None]
        # These centers of mass may not lie on the surface of the sphere,
        # but it can be shown that the constrained center of mass will
        # be a projection of this point along the surface normal in this
        # direction
        coms /= np.linalg.norm(coms, axis=1)[:, None]
        max_error = np.max(np.linalg.norm(points - coms, axis=1))
        msg = "Error ({}) exceeds tolerance {}".format(max_error, self.tolerance)
        self.assertLessEqual(max_error, self.tolerance, msg)


if __name__ == "__main__":
    unittest.main()

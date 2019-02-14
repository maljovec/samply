""" This module will test the functionality of samply.SCVTSampler
"""
import unittest
import samply
from sklearn import neighbors
import numpy as np


class TestSCVTSampler(unittest.TestCase):
    """ Class for testing the SCVT sampler
    """

    def setup(self):
        """
        """
        self.tolerance = 1e-1

    def test_2D(self):
        """
        """
        self.setup()
        n_samples = 20
        n_validation = 100000
        D = 2
        points = samply.SCVTSampler.generate_samples(
            n_samples, D, verbose=True
        )
        deltas = np.fabs(np.linalg.norm(points, axis=1) - 1)
        msg = "A generated point does not lie on the sphere"
        self.assertLessEqual(np.max(deltas), 1e-6, msg)
        sampler = samply.BallSampler(D)
        query_points = sampler.generate_samples(n_validation)

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
        # These centers of mass may not lie on the surface of the sphere,
        # but it can be shown that the constrained center of mass will
        # be a projection of this point along the surface normal in this
        # direction
        coms /= np.linalg.norm(coms, axis=1)[:, None]
        max_error = np.max(np.linalg.norm(points - coms, axis=1))
        msg = "Error ({}) exceeds tolerance {}".format(
            max_error, self.tolerance
        )
        self.assertLessEqual(max_error, self.tolerance, msg)


if __name__ == "__main__":
    unittest.main()

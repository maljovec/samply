""" This module will test the functionality of samply.CVTSampler
"""
import unittest
import samply
from sklearn import neighbors
import numpy as np


class TestCVTSampler(unittest.TestCase):
    """ Class for testing the CVT sampler using Monte Carlo sampling to
        quantify the area of the Voronoi cells.
    """

    def setup(self):
        """
        """
        self.tolerance = 1e-1

    def n_dimension_validation(self, points, query_points):
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

    def n_dimension_grid_validation(self, n_samples, n_validation, D):
        points = samply.CVTSampler.generate_samples(n_samples, D)
        n_grid_validation = int(np.ceil(n_validation ** (1. / D)))
        xi = np.linspace(0, 1, n_grid_validation)
        x = []
        for i in range(D):
            x.append(xi)
        grid = np.meshgrid(*x)
        print(grid)
        query_points = np.vstack(map(np.ravel, grid)).T
        self.n_dimension_validation(points, query_points)

    def n_dimension_mc_validation(self, n_samples, n_validation, D):
        points = samply.CVTSampler.generate_samples(n_samples, D)
        query_points = np.random.uniform(0, 1, (n_validation, D))
        self.n_dimension_validation(points, query_points)

    def test_verbosity(self):
        """
        """
        self.setup()
        points = samply.CVTSampler.generate_samples(10, 2, verbose=True)
        query_points = np.random.uniform(0, 1, (1000000, 2))
        self.n_dimension_validation(points, query_points)

    def test_2D_small(self):
        """
        """
        self.setup()
        # self.n_dimension_grid_validation(10, 100, 2)
        self.n_dimension_mc_validation(10, 100000, 2)

    def test_2D_moderate(self):
        """
        """
        self.setup()
        self.n_dimension_mc_validation(1000, 100000, 2)

    # Disable until more optimization can be done, this is too slow
    # right now.
    # def test_2D_large(self):
    #     """
    #     """
    #     self.setup()
    #     self.n_dimension_mc_validation(100000, 1000000, 2)

    def test_3D_small(self):
        """
        """
        self.setup()
        self.n_dimension_mc_validation(10, 100000, 3)

    def test_3D_moderate(self):
        """
        """
        self.setup()
        self.n_dimension_mc_validation(1000, 100000, 3)

    def test_4D_moderate(self):
        """
        """
        self.setup()
        self.n_dimension_mc_validation(1000, 1000000, 4)

    def test_5D_moderate(self):
        """
        """
        self.setup()
        self.n_dimension_mc_validation(1000, 1000000, 5)

if __name__ == "__main__":
    unittest.main()

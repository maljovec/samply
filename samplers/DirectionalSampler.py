import numpy as np


class DirectionalSampler(object):
    """
        A class for uniformly sampling the space of directions, useful for
        generating vectors

        Source: On decompositional algorithms for uniform sampling from
        n-spheres and n-balls
    """

    def __init__(self, dimensionality=2):
        """
        """
        self.dimensionality = dimensionality

    def generate_samples(self, count=1):
        if self.dimensionality == 1:
            return np.array([[-1], [1]])

        samples = np.zeros((count, self.dimensionality))
        for i in range(count):
            X = np.random.normal(0, 1, self.dimensionality)
            X /= np.linalg.norm(X)
            samples[i, :] = X

        return samples

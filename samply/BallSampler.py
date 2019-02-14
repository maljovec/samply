import numpy as np


class BallSampler(object):
    """
        A class for uniformly sampling a unit ball of arbitrary dimension

        Source: On decompositional algorithms for uniform sampling from
        n-spheres and n-balls
    """

    def __init__(self, dimensionality=2):
        """
        """
        self.dimensionality = dimensionality

    def generate_samples(self, count=1):
        samples = np.zeros((count, self.dimensionality))
        for i in range(count):
            X = np.random.normal(0, 1, self.dimensionality+2)
            X /= np.linalg.norm(X)
            samples[i, :] = X[0:self.dimensionality]

        return samples

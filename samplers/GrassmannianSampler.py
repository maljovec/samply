import numpy as np


class GrassmannianSampler(object):
    """
    """

    def __init__(self, data_dimensionality, target_dimensionality=2):
        """
        """
        self.data_dimensionality = data_dimensionality
        self.target_dimensionality = target_dimensionality

    def generate_samples(self, count=10000):
        """
        """
        basis = np.zeros((self.data_dimensionality,
                          self.target_dimensionality))
        basis[0, 0] = 1
        basis[1, 1] = 1
        samples = []
        # Using Shusen's notation from:
        # http://www.sci.utah.edu/~shusenl/publications/EuroVis-Grassmannian.pdf
        #   (Section 3.1 Uniform Sampling)
        for _ in range(count):
            S = np.random.randn(self.data_dimensionality,
                                self.data_dimensionality)
            Q, R = np.linalg.qr(S)
            # T = np.dot(Q,(np.diag(np.sign(np.diag(R)))))
            # Shorthand: we can exploit numpy's default broadcast
            # multiplication behavior to cut off a few cycles.
            T = Q*np.sign(np.diag(R))
            # I have no idea why this works, but Shusen's code also does it.
            # His explanation says something completely different, but maybe he
            # changed his mind? I would really like this to be more clear.
            # Why does flipping the sign of an arbitrary column ensure this?
            if np.linalg.det(T) < 0:
                cols = T.shape[1]
                T[:, int(cols/2)] = -T[:, int(cols/2)]
            samples.append(np.dot(Q, basis))
        return samples

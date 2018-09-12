import numpy as np
from .DirectionalSampler import DirectionalSampler
from .BallSampler import BallSampler


def gram_schmidt(vectors):
    """
        Do not use, this is numerically less stable than the
        'orthogonalize' method.
    """
    basis = []
    for v in vectors:
        w = v - np.sum(np.dot(v, b)*b for b in basis)
        if (w > 1e-10).any():
            basis.append(w/np.linalg.norm(w))
    return np.array(basis)


def orthogonalize(vectors):
    """
        This is a more stable version of the gram_schmidt function that
        instead uses the QR factorization to construct a set of
        orthonormal vectors where the first row is the same as that
        given by the first row of the input vectors. Thus, the remaining
        rows define a subspace that is orthogonal to the desired vector.
    """
    A = np.array(vectors).T
    Q, R = np.linalg.qr(A)
    return Q.T


class SubspaceSampler(object):
    """
        A class for uniformly sampling a unit ball of arbitrary
        dimension perpendicular to a defined vector

        Source: On decompositional algorithms for uniform sampling from
        n-spheres and n-balls
    """

    def __init__(self, vector):
        """
        """
        self.dimensionality = len(vector)
        self.subspace_basis = []

        if vector[-1] != 0:
            identity = np.eye(self.dimensionality-1, self.dimensionality)
        else:
            idx = np.nonzero(vector)[0]
            identity = np.eye(self.dimensionality, self.dimensionality)
            identity = np.delete(identity, idx, axis=0)

        vectors = np.vstack((vector, identity))
        # self.subspace_basis = gram_schmidt(vectors)[1:]
        self.subspace_basis = orthogonalize(vectors)[1:]
        if len(self.subspace_basis) == 0:
            raise ValueError('Could not construct valid subspace.')

    def generate_samples(self, count=1, sampler=None):
        if sampler is None:
            sampler = BallSampler(self.dimensionality-1)

        pseudoSamples = sampler.generate_samples(count)

        # In case the sampler overrides the user's count, make sure this is
        # the size of pseudoSamples, since the case where D=1 and the sampler
        # is directional, we only have two options (backward and forward)
        samples = np.zeros((len(pseudoSamples), self.dimensionality))
        for i, Xi in enumerate(pseudoSamples):
            samples[i, :] = np.dot(Xi, self.subspace_basis)

        return samples

    def generate_ball_samples(self, count=1):
        return self.generate_samples(count, BallSampler(self.dimensionality-1))

    def generate_directional_samples(self, count=1):
        return self.generate_samples(count,
                                     DirectionalSampler(self.dimensionality-1))

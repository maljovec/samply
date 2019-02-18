import numpy as np
from samply import ball, directional


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


def grassmannian(count=1, data_dimensionality=2, target_dimensionality=2):
    """
    """
    basis = np.zeros((data_dimensionality, target_dimensionality))
    basis[0, 0] = 1
    basis[1, 1] = 1
    samples = []
    # Using Shusen's notation from:
    # http://www.sci.utah.edu/~shusenl/publications/EuroVis-Grassmannian.pdf
    #   (Section 3.1 Uniform Sampling)
    for _ in range(count):
        S = np.random.randn(data_dimensionality, data_dimensionality)
        Q, R = np.linalg.qr(S)
        # T = np.dot(Q,(np.diag(np.sign(np.diag(R)))))
        # Shorthand: we can exploit numpy's default broadcast
        # multiplication behavior to cut off a few cycles.
        T = Q * np.sign(np.diag(R))
        # I have no idea why this works, but Shusen's code also does it.
        # His explanation says something completely different, but maybe he
        # changed his mind? I would really like this to be more clear.
        # Why does flipping the sign of an arbitrary column ensure this?
        if np.linalg.det(T) < 0:
            cols = T.shape[1]
            T[:, int(cols / 2)] = -T[:, int(cols / 2)]
        samples.append(np.dot(Q, basis))
    return samples


def orthogonal_ball(vector, count=1):
    """
    """
    dimensionality = len(vector)
    subspace_basis = []

    if vector[-1] != 0:
        identity = np.eye(dimensionality - 1, dimensionality)
    else:
        idx = np.nonzero(vector)[0]
        identity = np.eye(dimensionality, dimensionality)
        identity = np.delete(identity, idx, axis=0)

    vectors = np.vstack((vector, identity))
    subspace_basis = orthogonalize(vectors)[1:]
    if len(subspace_basis) == 0:
        raise ValueError("Could not construct valid subspace.")

    pseudoSamples = ball.uniform(count, dimensionality - 1)

    # In case the sampler overrides the user's count, make sure this is
    # the size of pseudoSamples, since the case where D=1 and the sampler
    # is directional, we only have two options (backward and forward)
    samples = np.zeros((len(pseudoSamples), dimensionality))
    for i, Xi in enumerate(pseudoSamples):
        samples[i, :] = np.dot(Xi, subspace_basis)

    return samples


def orthogonal_directional(vector, count=1):
    """
    """
    dimensionality = len(vector)
    subspace_basis = []

    if vector[-1] != 0:
        identity = np.eye(dimensionality - 1, dimensionality)
    else:
        idx = np.nonzero(vector)[0]
        identity = np.eye(dimensionality, dimensionality)
        identity = np.delete(identity, idx, axis=0)

    vectors = np.vstack((vector, identity))
    subspace_basis = orthogonalize(vectors)[1:]
    if len(subspace_basis) == 0:
        raise ValueError("Could not construct valid subspace.")

    pseudoSamples = directional.uniform(count, dimensionality - 1)

    # In case the sampler overrides the user's count, make sure this is
    # the size of pseudoSamples, since the case where D=1 and the sampler
    # is directional, we only have two options (backward and forward)
    samples = np.zeros((len(pseudoSamples), dimensionality))
    for i, Xi in enumerate(pseudoSamples):
        samples[i, :] = np.dot(Xi, subspace_basis)

    return samples


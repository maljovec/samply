import numpy as np


def uniform(count=1, dimensionality=2):
    samples = np.zeros((count, dimensionality))
    for i in range(count):
        X = np.random.normal(0, 1, dimensionality + 2)
        X /= np.linalg.norm(X)
        samples[i, :] = X[0:dimensionality]

    return samples

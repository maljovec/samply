import numpy as np
from sklearn import neighbors


def uniform(count=1, dimensionality=2):
    if dimensionality == 1:
        return np.array([[-1], [1]])

    samples = np.zeros((count, dimensionality))
    for i in range(count):
        X = np.random.normal(0, 1, dimensionality)
        X /= np.linalg.norm(X)
        samples[i, :] = X

    return samples


def cvt(
    count=1,
    dimensionality=2,
    max_iterations=1000000,
    epsilon=1e-6,
    verbose=False,
    update_size=10000,
):
    points = uniform(count, dimensionality)
    nn = neighbors.NearestNeighbors(n_neighbors=1)
    nn.fit(points)

    ji = np.ones(count)
    error = np.ones(count)
    maxErrorId = -1
    maxError = 0.0

    query_points = uniform(update_size, dimensionality)
    sites = nn.kneighbors(query_points, return_distance=False)

    for i in range(max_iterations):
        if verbose and i % update_size == 0 and i > 0:
            print("Iter {} err = {}".format(i, np.sqrt(maxError)))

        p = query_points[i % update_size]
        closest = sites[i % update_size]

        px = np.array(points[closest])
        points[closest] = (ji[closest] * px + p) / (ji[closest] + 1)
        sumdiff = np.sum(px - points[closest]) ** 2

        if i % update_size == 0:
            nn.fit(points)
            query_points = uniform(update_size, dimensionality)
            sites = nn.kneighbors(query_points, return_distance=False)

        ji[closest] = ji[closest] + 1

        if epsilon > 0:
            error[closest] = sumdiff

            # Approximation of the max error without the need to
            # traverse all of the points
            if maxErrorId == closest:
                maxError = error[closest]
            elif error[closest] > maxError:
                maxErrorId = closest
                maxError = error[closest]

            if maxError < epsilon**2:
                if verbose:
                    print("Converged at {} err = {}".format(i, np.sqrt(maxError)))
                break

    if verbose:
        nn = neighbors.NearestNeighbors(n_neighbors=2)
        nn.fit(points)
        distances, _ = nn.kneighbors(points, return_distance=True)
        maximinDist = np.max(distances[:, 1])

        print("maximin distance = {}".format(maximinDist))
    return points / np.expand_dims(np.linalg.norm(points, axis=1), axis=1)

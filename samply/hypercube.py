from sklearn import neighbors
import numpy as np
import pyDOE
import ghalton


def uniform(count=1, dimensionality=2):
    return np.random.uniform(size=(count, dimensionality))


def grid(count=1, dimensionality=2):
    numPoints = np.ceil(count ** (1. / dimensionality))
    temp = np.meshgrid(
        *[np.linspace(0, 1, numPoints)[:] for i in range(dimensionality)]
    )
    return np.vstack(map(np.ravel, temp)).T[:count]


def cvt(
    count=1,
    dimensionality=2,
    max_iterations=1000000,
    epsilon=1e-6,
    verbose=False,
    update_size=10000,
):
    points = np.random.uniform(0, 1, size=(count, dimensionality))
    nn = neighbors.NearestNeighbors(n_neighbors=1)
    nn.fit(points)

    ji = np.ones(count)
    error = np.ones(count)
    maxErrorId = -1
    maxError = 0.0

    query_points = np.random.uniform(0, 1, size=(update_size, dimensionality))
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
            query_points = np.random.uniform(
                0, 1, size=(update_size, dimensionality)
            )
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

            if maxError < epsilon ** 2:
                if verbose:
                    print(
                        "Converged at {} err = {}".format(i, np.sqrt(maxError))
                    )
                break

    if verbose:
        nn = neighbors.NearestNeighbors(n_neighbors=2)
        nn.fit(points)
        distances, _ = nn.kneighbors(points, return_distance=True)
        maximinDist = np.max(distances[:, 1])

        print("maximin distance = {}".format(maximinDist))
    return points


def lhs(count=1, dimensionality=2):
    return pyDOE.lhs(dimensionality, count)


def halton(count=1, dimensionality=2, seed=0):
    sequencer = ghalton.GeneralizedHalton(dimensionality, seed)
    return np.array(sequencer.get(count))

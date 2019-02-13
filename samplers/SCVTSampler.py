from sklearn import neighbors
import numpy as np
from samplers.DirectionalSampler import DirectionalSampler


class SCVTSampler(object):
    """
        A class for performing Surface Centroidal Voronoi Tessellation
        sampling in arbitrary dimension.
    """

    @classmethod
    def generate_samples(
        self,
        count=1,
        dimensionality=2,
        seed=0,
        max_iterations=1000000,
        epsilon=1e-6,
        verbose=False,
    ):
        np.random.seed(seed)
        sampler = DirectionalSampler(dimensionality)

        points = sampler.generate_samples(count)
        nn = neighbors.NearestNeighbors(n_neighbors=1)
        nn.fit(points)

        ji = np.ones(count)
        error = np.ones(count)
        maxErrorId = -1
        maxError = 0.0

        for i in range(max_iterations):
            if verbose and i % 10000 == 0:
                print("Iter {} err = {}".format(i, np.sqrt(maxError)))

            p = np.atleast_2d(sampler.generate_samples(1))

            # find closest
            closest = nn.kneighbors(p, return_distance=False)[0]

            sumdiff = 0
            px = np.array(points[closest])
            points[closest] = (ji[closest] * px + p) / (ji[closest] + 1)
            sumdiff = np.sum(px - points[closest]) ** 2

            if i % 10000 == 0:
                nn.fit(points)

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
                            "Converged at {} err = {}".format(
                                i, np.sqrt(maxError)
                            )
                        )
                    break

        if verbose:
            nn = neighbors.NearestNeighbors(n_neighbors=2)
            nn.fit(points)
            distances, indices = nn.kneighbors(points, return_distance=True)
            maximinDist = np.max(distances[:, 1])

            print("maximin distance = {}".format(maximinDist))
        return points / np.expand_dims(np.linalg.norm(points, axis=1), axis=1)

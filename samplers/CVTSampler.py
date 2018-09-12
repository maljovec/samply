import numpy as np
import subprocess
import os


class CVTSampler(object):
    """
        A class for performing Centroidal Voronoi Tessellation sampling
        in arbitrary dimension.
    """
    @classmethod
    def generate_samples(self, count=1, dimensionality=2, seed=0):
        path = os.path.dirname(os.path.abspath(__file__))
        cmd = os.path.join(path, 'cvt', 'createCVT')
        result = subprocess.run([cmd,
                                 '-N', str(count),
                                 '-D', str(dimensionality),
                                 '-seed', str(seed),
                                 '-ann', '1',
                                 '-iterations', '1000000'],
                                stdout=subprocess.PIPE)
        lines = result.stdout.decode('utf-8').strip().split('\n')
        X = np.zeros((count, dimensionality))
        for i, line in enumerate(lines):
            X[i, :] = list(map(float, line.strip().split(' ')))
        return X

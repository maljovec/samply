# samplers
A Collection of Space-filling Sampling Designs for Arbitrary Dimensions.

Including:
 * Uniform sampling of a n-dimensional ball
 * Uniform sampling of the directions on an n-dimensional sphere
 * Sampling the Grassmannian Atlas
 * An approximate Centroidal Voronoi Tessellation using a Probabilistic
   Lloyd's Algorithm
 * An approximate Constrained Centroidal Voronoi Tessellation on an
   n-sphere

Forthcoming:
 * A unified interface for Latin Hypercube sampling from PyDOE
 * A unified interface for Generalized Halton sequence sampling from ghalton
 * A test suite to verify results in low to moderate dimensionality
 * Improved code documentation

The python CVT code is adapted from a C++ implementation provided by
Carlos Correa. The Grassmannian sampler is adapted from code from Shusen
Liu.

:warning: **NOTE**: This code is experimental, minimally tested, and
ill-documented. **Use at your own risk!** :warning:

# Prerequisites

 * [ghalton](https://github.com/fmder/ghalton)
 * [pyDOE](https://pythonhosted.org/pyDOE/)

You can install these using the follow pip command:

 ```bash
 pip install ghalton pyDOE
 ```

# Installation

```bash
git clone https://github.com/maljovec/samplers.git
cd samplers
python setup.py [build|develop|install]
```

# Testing

The test suite can be run through the setup script:

```bash
python setup.py test
```

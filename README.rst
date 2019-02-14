=====
nglpy
=====

.. badges

.. image:: https://img.shields.io/pypi/v/samply.svg
        :target: https://pypi.python.org/pypi/samply
        :alt: PyPi
.. image:: https://travis-ci.org/maljovec/samply.svg?branch=master
        :target: https://travis-ci.org/maljovec/samply
        :alt: Travis-CI
.. image:: https://coveralls.io/repos/github/maljovec/samply/badge.svg?branch=master
        :target: https://coveralls.io/github/maljovec/samply?branch=master
        :alt: Coveralls
.. image:: https://readthedocs.org/projects/samply/badge/?version=latest
        :target: https://samply.readthedocs.io/en/latest/?badge=latest
        :alt: ReadTheDocs
.. image:: https://pyup.io/repos/github/maljovec/samply/shield.svg
        :target: https://pyup.io/repos/github/maljovec/samply/
        :alt: Pyup

.. end_badges

.. logo

.. image:: docs/_static/samplers.svg
    :align: center
    :alt: samplers

.. end_logo

.. introduction

A Python library for generating space-filling sample sets of low to moderate
dimensional data from domains including:
 * Euclidean space
 * Grassmannian atlas
 * Surface of an n-Sphere

.. LONG_DESCRIPTION

A Collection of Space-filling Sampling Designs for Arbitrary Dimensions.

Including:
 * Uniform sampling of a n-dimensional ball
 * Uniform sampling of the directions on an n-dimensional sphere
 * Sampling the Grassmannian Atlas
 * An approximate Centroidal Voronoi Tessellation using a Probabilistic
   Lloyd's Algorithm
 * An approximate Constrained Centroidal Voronoi Tessellation on an
   n-sphere

The python CVT code is adapted from a C++ implementation provided by
Carlos Correa. The Grassmannian sampler is adapted from code from Shusen
Liu.

.. END_LONG_DESCRIPTION

.. end_introduction

.. install

Installation
============

::

    git clone https://github.com/maljovec/samplers.git
    cd samplers
    python setup.py [build|develop|install]

.. end-install

.. usage

Usage
=====

Then you can use the library from python such as the example below::

    import nglpy
    import numpy as np

    point_set = np.random.rand(100,2)
    max_neighbors = 9
    beta = 1

    # TODO: Make this an enum, remove hard-coding
    graph_type = 'beta skeleton'

    aGraph = nglpy.Graph(point_set, graph_type, max_neighbors, beta)

    aGraph.neighbors()

.. end-usage


.. testing

Testing
=====

The test suite can be run through the setup script:

    python setup.py test

.. end-testing

.. todo

What's Next
======

Forthcoming:
 * A unified interface for Latin Hypercube sampling from PyDOE
 * A unified interface for Generalized Halton sequence sampling from ghalton
 * A test suite to verify results in low to moderate dimensionality
 * Improved code documentation

.. end-todo

=====
samply
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

.. image:: docs/_static/samply.svg
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
The API is structured such that the top level packages represent the shape
of the domain you are interested in:

 * ball - The n-dimensional solid unit ball
 * directional - The space of unit length directions in n-dimensional space.
   You can also consider this a sampling of the boundary of the n-dimensional
   unit ball.
 * hypercube - The n-dimensional solid unit hypercube :math:`x \\in [0,1]^n`.
 * subspace - Sampling a n-1-dimensional subspace orthogonal to a unit vector
   or sampling the Grassmanian Atlas of projections from a dimension n to a
   lower dimension m.
 * shape - a collection of (n-1)-manifold and non-manifold shapes embedded in
   an n dimensional space. For now these must all be sampled using a uniform
   distribution.

Within each module is a list of ways to fill the space of the samples.
Note, that not all of the methods listed below are applicable to the modules
listed above. They include:

 * Uniform - a random, uniform distribution of points (available for ball,
   directional, hypercube, subspace, and shape)
 * Normal - a Gaussian distribution of points (available for hypercube)
 * Multimodal - a mixture of Gaussian distributions of points (available for hypercube)
 * CVT - an approximate centroidal Voronoi tessellation of the points
   constrained to the given space (available for hypercube and directional)
 * LHS - a Latin hypercube sampling design of points constrained to the space
   (available for hypercube)
 *

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

    import samply

    sampler = samply.DirectionalSampler(2)
    direction_samples = sampler.generate_samples(10000)

    sampler = samply.BallSampler(2)
    ball_samples = sampler.generate_samples(10000)

    sampler = samply.BallSampler(2)
    ball_samples = sampler.generate_samples(10000)

    sampler = samply.GrassmannianSampler(3, 2)
    projection_samples = sampler.generate_samples(10)

    cvt_samples = samply.CVTSampler.generate_samples(10, 2)

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

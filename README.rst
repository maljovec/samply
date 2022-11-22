=======
samply
=======

.. badges

.. image:: https://img.shields.io/pypi/v/samply.svg
        :target: https://pypi.python.org/pypi/samply
        :alt: Latest Version on PyPI
.. image:: https://img.shields.io/pypi/dm/samply.svg?label=PyPI%20downloads
        :target: https://pypi.org/project/samply/
        :alt: PyPI downloads

.. image:: https://github.com/maljovec/samply/actions/workflows/quality.yaml/badge.svg?branch=main
        :target: https://github.com/maljovec/samply/actions
        :alt: Code Quality Test Results
.. image:: https://github.com/maljovec/samply/actions/workflows/test.yaml/badge.svg?branch=main
        :target: https://github.com/maljovec/samply/actions
        :alt: Test Suite Results

.. image:: https://www.codefactor.io/repository/github/maljovec/samply/badge
        :target: https://www.codefactor.io/repository/github/maljovec/samply
        :alt: CodeFactor
.. image:: https://coveralls.io/repos/github/maljovec/samply/badge.svg?branch=main
        :target: https://coveralls.io/github/maljovec/samply?branch=main
        :alt: Coveralls
.. image:: https://readthedocs.org/projects/samply/badge/?version=latest
        :target: https://samply.readthedocs.io/en/latest/?badge=latest
        :alt: ReadTheDocs
.. image:: https://pyup.io/repos/github/maljovec/samply/shield.svg
        :target: https://pyup.io/repos/github/maljovec/samply/
        :alt: Pyup

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
        :target: https://github.com/psf/black
        :alt: This code is formatted in black
.. image:: https://img.shields.io/badge/License-BSD_3--Clause-blue.svg
        :target: https://opensource.org/licenses/BSD-3-Clause
        :alt: BSD 3-Clause License

.. end_badges

.. logo

.. .. image:: docs/_static/samply.svg
..    :align: center
..    :alt: samply

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
* directional - The space of unit length directions in n-dimensional space. You can also consider this a sampling of the boundary of the n-dimensional unit ball.
* hypercube - The n-dimensional solid unit hypercube :math:`x \\in [0,1]^n`.
* subspace - Sampling a n-1-dimensional subspace orthogonal to a unit vector or sampling the Grassmanian Atlas of projections from a dimension n to a lower dimension m.
* shape - a collection of (n-1)-manifold and non-manifold shapes embedded in an n dimensional space. For now these must all be sampled using a uniform distribution.

Within each module is a list of ways to fill the space of the samples.
Note, that not all of the methods listed below are applicable to the modules
listed above. They include:

* Uniform - a random, uniform distribution of points (available for ball, directional, hypercube, subspace, and shape)
* Normal - a Gaussian distribution of points (available for hypercube)
* Multimodal - a mixture of Gaussian distributions of points (available for hypercube)
* CVT - an approximate centroidal Voronoi tessellation of the points constrained to the given space (available for hypercube and directional)
* LHS - a Latin hypercube sampling design of points constrained to the space (available for hypercube)

The python CVT code is adapted from a C++ implementation provided by
Carlos Correa. The Grassmannian sampler is adapted from code from Shusen
Liu.

.. END_LONG_DESCRIPTION

.. end_introduction

.. install

Installation
============

A preliminary version is available on PyPI::

    pip install samply

Otherwise, you can download the repository for the most cutting edge additions::

    git clone https://github.com/maljovec/samply.git
    cd samply
    python setup.py [build|develop|install]

.. end-install

.. usage

Usage
=====

You can use the library from python such as the examples below::

    import samply

    direction_samples = samply.directional.uniform(10000, 2)
    ball_samples = samply.ball.uniform(10000, 2)
    scvt_samples = samply.directional.cvt(10000, 2)
    cvt_samples = samply.hypercube.cvt(10000, 2)

    projection_samples = samply.subspace.grassmannian(10000, 3, 2)

The ``*samples`` variables will be NxD matrices where N is the number of samples requested and D is the dimensionality of the sampler or the requested dimensionality.

.. end-usage


.. testing

Testing
=======

The test suite can be run through the setup script::

    python setup.py test

.. end-testing

.. example

Example
=======

To test drive a subset of the different samplers in action, check out this little `web app <https://samply.appspot.com/>`_ hosted on the Google Cloud Platform which is using samply under the covers. Note, the CVT is still rather inefficient for larger sample sizes.

.. end-example

.. todo

What's Next
===========

Forthcoming:
 * Improved documentation

.. end-todo

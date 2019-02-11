# samplers
A Collection of Space-filling Sampling Designs for Arbitrary Dimensions.

CVT C++ code is adapted from a library provided by Carlos Correa.

:warning: **NOTE**: This code is experimental, poorly designed, does not follow any best practices, minimally tested, and ill-documented. **Use at your own risk!** :warning: 

# Prerequisites

 * [ANN](https://www.cs.umd.edu/~mount/ANN/)
 * [ghalton](https://github.com/fmder/ghalton)
 * [pyDOE](https://pythonhosted.org/pyDOE/)
 
 On Ubuntu:
 ```bash
 apt install libann-dev
 pip install ghalton pyDOE
 ```
 YMMV on other OSes.
 
# Installation

```bash
git clone https://github.com/maljovec/samplers.git
cd samplers
pushd samplers/cvt
make
popd
# Only tested develop, I'm not sure if install will work because I make no effort to move the createCVT executable.
python setup.py [build|develop|install]
```

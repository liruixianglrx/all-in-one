from distutils.core import Extension, setup
from distutils import sysconfig

import numpy

_eco_ext = Extension(
    "_eco_ext",
    ["eco_ext.i", "./eco_ext/eco_ext.c"],
    include_dirs=[numpy.get_include()],
)

# NumyTypemapTests setup
setup(
    name="eco_ext function",
    description="Supplementary functions for ECO",
    author="Yaotian Liu",
    version="0.1",
    ext_modules=[_eco_ext],
)

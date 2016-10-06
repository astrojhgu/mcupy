#!/usr/bin/env python

import sys
from distutils.core import setup, Extension


if sys.version_info[0]==3:
    boost_python_lib='boost_python3'
else:
    boost_python_lib='boost_python'


module1=Extension('mcupy.core',
                      include_dirs=['../mcmc_utilities','../east/include','../coscalcpp/include'],
                      libraries=[boost_python_lib,'east','coscalcpp'],
                      library_dirs=['../east/lib','../coscalcpp/lib'],
                      extra_compile_args=['-std=c++14'],
                      sources=['mcmc.cpp'],
                      language='c++')

setup(name='core',
          packages=['mcupy'],
          version='1.0',
          ext_modules=[module1])

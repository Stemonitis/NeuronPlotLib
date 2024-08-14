#!/usr/bin/env python

from setuptools import setup
from src.NeuronPlotLib._version import __version__

# read version info from project code
# exec(open('src/NeuronPlotLib/_version.py').read())

setup_cmdclass = {}

setup(
    version=__version__,
    # cmdclass = setup_cmdclass,
)

#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

import clikraken

# I really prefer Markdown to reStructuredText.  PyPi does not.  This allows me
# to have things how I'd like, but not throw complaints when people are trying
# to install the package and they don't have pypandoc or the README in the
# right place.
try:
    import pypandoc
    long_description = pypandoc.convert_file('README.md', 'rst')
except (IOError, ImportError):
    long_description = open('README.md').read()

setup(
    name='clikraken',
    version=clikraken.__version__,
    packages=['clikraken', 'clikraken.api', 'clikraken.api.private', 'clikraken.api.public'],
    author='Marc Gallet',
    author_email='zertrin@gmail.com',
    license='Apache 2.0',
    description='Command-line client for the Kraken exchange',
    long_description=long_description,
    include_package_data=True,
    url='https://github.com/zertrin/clikraken',
    install_requires=[
        'krakenex',
        'arrow',
        'tabulate',
        'colorlog',
    ],
    classifiers=[
        "Programming Language :: Python",
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Topic :: Office/Business :: Financial",
        "Topic :: Office/Business :: Financial :: Investment",
    ],
    entry_points={
        'console_scripts': [
            'clikraken=clikraken.clikraken:main',
        ],
    },
)

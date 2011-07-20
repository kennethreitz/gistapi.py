#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

from distutils.core import setup


def publish():
    """Publish to PyPi"""
    os.system("python setup.py sdist upload")


if sys.argv[-1] == "publish":
    publish()
    sys.exit()

    
required = ['requests', 'iso8601']


if sys.version_info[:2] < (2,6):
    required.append('simplejson')


setup(
    name='gistapi',
    version='0.2.4',
    description='Python wrapper for Gist API',
    long_description=open('README.rst').read() + '\n\n' + open('HISTORY.rst').read(),
    author='Kenneth Reitz',
    author_email='me@kennethreitz.com',
    url='http://github.com/kennethreitz/gistapi.py',
    packages=['gistapi'],
    install_requires=required,
    license='MIT',
    classifiers=(
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.5",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
    )
)

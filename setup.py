#!/usr/bin/env python
# encoding: utf-8

import os
import sys

from distutils.core import setup

def publish():
	"""Publish to PyPi"""
	os.system("python setup.py sdist upload")

if sys.argv[-1] == "publish":
	publish()
	sys.exit()

setup(name='gist',
	  version='0.6.2',
	  description='Python wrapper for Gist API',
	  long_description=open('README.mkd').read() + '\n\n' + open('HISTORY.mkd').read(),
	  author='Kenneth Reitz',
	  author_email='me@kennethreitz.com',
	  url='http://github.com/kennethreitz/gist.py',
	  packages=['gist'],
	  license='MIT',
	  classifiers = ( 
		"Development Status :: 4 - Beta",
		"License :: OSI Approved :: MIT License",
		"Programming Language :: Python",
		"Programming Language :: Python :: 2.5",
		"Programming Language :: Python :: 2.6",
		"Programming Language :: Python :: 2.7",
		)
	 )

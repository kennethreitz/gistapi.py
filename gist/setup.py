from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(name='gist',
      version=version,
      description="Python wrapper for Gist API",
      long_description="""\
Python wrapper for GitHub's Gist API""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='Gist API Wrapper GitHub',
      author='Kenneth Reitz',
      author_email='ping@kennethreitz.com',
      url='http://kennethreitz.com',
      license='',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=True,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )

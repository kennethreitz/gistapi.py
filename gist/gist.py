#!/usr/bin/env python
# encoding: utf-8

"""
Gist.py -- A Python wrapper for the Gist API
(c) 2010 Kenneth Reitz. MIT License.
"""

import simplejson, urllib
from cStringIO import StringIO

__version__ = "$Revision: 68852 $"

class Gists(object):
	"""Gist API wrapper"""
	def __init__(self, username=None, token=None):
		# raise NotImplementedError
		self._username = username; self._token = token
		
		
	def __repr__(self):
		pass
	
	def __str__(self):
		pass
		
	def fetch_gists_by_user():
		pass
		
class Gist(object):
	"""Base Gist Object"""
	def __init__(self, id):
		self.id = id
		self.url = 'http://github.com/{0}'.format(id)
		self.embed_url = 'http://github.com/{0}.js'.format(id)
		self._get_meta()

	def _get_meta(self):
		_meta_url = 'http://gist.github.com/api/v1/json/{0}'.format(self.id)
		_meta = simplejson.load(urllib.urlopen(_meta_url))['gists'][0]
		
		[setattr(self, attr, _meta[attr]) for attr in _meta.iterkeys()]
	
	
	
if __name__ == '__main__':
	
	gist = Gist(347430)
	
	print gist.files
	

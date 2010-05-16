#!/usr/bin/env python
# encoding: utf-8

"""
Gist.py -- A Python wrapper for the Gist API
(c) 2010 Kenneth Reitz. CC License.
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
	
	def __getattribute__(self, name):
		"""Gets attributes, but only if needed"""

		# Only make API call if needed
		if name in ['description', 'created_at', 'public', 'files', 'repo']: 
			if not hasattr(self, '_meta'):
				self._meta = self._get_meta()
				# self._meta = self._get_files
			
		return object.__getattribute__(self, name)

	def _get_meta(self):
		"""Fetches Gist metadata"""
		_meta_url = 'http://gist.github.com/api/v1/json/{0}'.format(self.id)
		_meta = simplejson.load(urllib.urlopen(_meta_url))['gists'][0]
		
		# Get all response properties
		for key, value in _meta.iteritems(): 
			
			# Change filename key for object instantiation
			if key == 'files': setattr(self, 'filenames', value)
			else: setattr(self, key, value)
			
		return True
	
	@property
	def files(self):
		
		files = {}
		
		for fn in self.filenames:
			uri = 'http://gist.github.com/raw/{0}/{1}'.format(self.id, fn)
			files[fn] = (urllib.urlopen(uri).read())
			
			# setattr(self, 'filenames', None)
		return files
	

# class File(object, filename, gist):
# 	def __init__(self):
# 		self.filename = filename
# 		self.url
# 		
# 
if __name__ == '__main__':
	
	gist = Gist(347430)
	
	print gist.description
	print gist.files
	

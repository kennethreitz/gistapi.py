#!/usr/bin/env python
# encoding: utf-8

"""
GistAPI.py -- A Python wrapper for the Gist API
(c) 2010 Kenneth Reitz. MIT License.

Example usage:

>>> Gist('d4507e882a07ac6f9f92').repo
'd4507e882a07ac6f9f92'

>>> Gist('d4507e882a07ac6f9f92').description
'Example Gist for gist.py'

>>> Gist('d4507e882a07ac6f9f92').created_at
'2010/05/16 10:51:15 -0700'

>>> Gist('d4507e882a07ac6f9f92').public
False

>>> Gist('d4507e882a07ac6f9f92').filenames
['exampleEmptyFile', 'exampleFile']

>>> Gist('d4507e882a07ac6f9f92').files
{'exampleFile': 'Example file content.', 'exampleEmptyFile': ''}

>>> Gists.fetch_by_user('kennethreitz')[-1].description
'My .bashrc configuration'
"""

import urllib

try: import simplejson as json
except ImportError: import json

class Gist(object):
	"""Gist Object"""
	
	def __init__(self, id=None, json=None):
		self.id = id; self._json = json
		

		# Map given repo id to gist id if none exists
		if self._json: self.id = json['repo']
	
	def __getattribute__(self, name):
		"""Gets attributes, but only if needed"""

		# Only make external API calls if needed
		if name in ['description', 'created_at', 'public', 'files', 'filenames', 'repo']: 
			if not hasattr(self, '_meta'):
				self._meta = self._get_meta()
			
		return object.__getattribute__(self, name)

	def _get_meta(self):
		"""Fetches Gist metadata"""
		
		# Use json data provided if available
		if self._json:
			_meta = self._json 
			setattr(self, 'id', _meta['repo'])
		else:
			# Fetch Gist metadata
			_meta_url = 'http://gist.github.com/api/v1/json/{0}'.format(self.id)
			_meta = json.load(urllib.urlopen(_meta_url))['gists'][0]
			
		self.url = 'http://github.com/{0}'.format(self.id)
		self.embed_url = 'http://github.com/{0}.js'.format(self.id)
		self.json_url = 'http://github.com/{0}.json'.format(self.id)
		
		for key, value in _meta.iteritems(): 
			
			if key == 'files': 
				# Remap file key from API
				setattr(self, 'filenames', value)
			else:
				# Attach properties to object
				setattr(self, key, value)
			
		return _meta
	
	@property
	def files(self):
		"""Fetches a gists files and stores them in the 'files' property"""
		files = {}
		
		for fn in self.filenames:
			# Grab file contents
			file_url = 'http://gist.github.com/raw/{0}/{1}'.format(self.id, fn)
			files[fn] = (urllib.urlopen(file_url).read())
			
		return files
	

class Gists(object):
	"""Gist API wrapper"""
	def __init__(self, username=None, token=None):
		# Token-based Authentication is unnecesary at this point, gist api functionality is still in alpha
		self._username = username; self._token = token

	@staticmethod
	def fetch_by_user(name):
		"""Returns a set of public Gist objects owned by the given GitHub username"""

		_url = 'http://gist.github.com/api/v1/json/gists/{0}'.format(name)
		
		# Return a list of Gist objects 
		return [Gist(json=g) for g in json.load(urllib.urlopen(_url))['gists']]


if __name__ == '__main__':
	import doctest
	doctest.testmod()
	
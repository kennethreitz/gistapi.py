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
		# Token-based Authentication is unnecesary at this point, gist api functionality is still in alpha
		self._username = username; self._token = token
	
	@staticmethod
	def fetch_by_user(name):
		_url = 'http://gist.github.com/api/v1/json/gists/{0}'.format(name)
		
		# print simplejson.load(urllib.urlopen(_url))['gists'][0]
		# collection = []
		# for g in simplejson.load(urllib.urlopen(_url))['gists']:
			# collection.append(Gist(json=g))
			
		return [Gist(json=g) for g in simplejson.load(urllib.urlopen(_url))['gists']]
			
		# return collection
		

		
class Gist(object):
	"""Base Gist Object"""
	def __init__(self, id=None, json=None):
		self.id = id; self._json = json
		self.url = 'http://github.com/{0}'.format(id)
		self.embed_url = 'http://github.com/{0}.js'.format(id)
		
		if self._json:
			self.id = json['repo']
	
	def __getattribute__(self, name):
		"""Gets attributes, but only if needed"""

		# Only make API call if needed
		if name in ['description', 'created_at', 'public', 'files', 'filenames', 'repo']: 
			if not hasattr(self, '_meta'):
				self._meta = self._get_meta()
				# self._meta = self._get_files
			
		return object.__getattribute__(self, name)

	def _get_meta(self):
		"""Fetches Gist metadata"""
		if self._json:
			_meta = self._json 
			setattr(self, 'id', _meta['repo'])
		else:
			_meta_url = 'http://gist.github.com/api/v1/json/{0}'.format(self.id)
			_meta = simplejson.load(urllib.urlopen(_meta_url))['gists'][0]
		
		# Get all response properties
		for key, value in _meta.iteritems(): 
			
			# Change filename key for object instantiation
			if key == 'files': setattr(self, 'filenames', value)
			else: setattr(self, key, value)
			
		return _meta
	
	@property
	def files(self):
		"""Fetches a gists files and stores them in the 'files' property"""
		files = {}
		
		for fn in self.filenames:
			file_url = 'http://gist.github.com/raw/{0}/{1}'.format(self.id, fn)
			files[fn] = (urllib.urlopen(file_url).read())
			
		return files
	

if __name__ == '__main__':
	
	# gist = Gist('399505')
	# print gist.id
	# print gist.description
	# print gist.files 
	
	# a = Gists.fetch_by_user('kennethreitz')
	# print a[]
	# print dir(a)
	# print a.id
	# print a.description
	# 	
	for gist in Gists.fetch_by_user('kennethreitz'):
		# print gist.id
		print gist.description
		# print gist.files

	# print gist.id
	# print gist.filenames
	# print gist.files

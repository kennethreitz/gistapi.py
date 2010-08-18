# encoding: utf-8

"""
GistAPI.py -- A Python wrapper for GitHub's Gist API
(c) 2010 Kenneth Reitz. MIT License.

Example usage:

>>> Gist('d4507e882a07ac6f9f92').repo
u'd4507e882a07ac6f9f92'

>>> Gist('d4507e882a07ac6f9f92').owner
u'kennethreitz'

>>> Gist('d4507e882a07ac6f9f92').description
u'Example Gist for gist.py'

>>> Gist('d4507e882a07ac6f9f92').created_at.isoformat()
'2010-05-16T10:51:15-07:00'

>>> Gist('d4507e882a07ac6f9f92').public
False

>>> Gist('d4507e882a07ac6f9f92').filenames
['exampleEmptyFile', 'exampleFile']

>>> Gist('d4507e882a07ac6f9f92').files
{'exampleFile': u'Example file content.', 'exampleEmptyFile': u''}

>>> Gists.fetch_by_user('kennethreitz')[-1].description
u'My .bashrc configuration'
"""


import urllib
from dateutil.parser import parse as dtime


try:
    import simplejson as json
except ImportError:
    import json



__all__ = ['Gist', 'Gists']


class Gist(object):
    """Gist Object"""

    def __init__(self, id=None, json=None):
        self.id = id
        self._json = json

        # Map given repo id to gist id if none exists
        if self._json:
            self.id = json['repo']

    def __getattribute__(self, name):
        """Gets attributes, but only if needed"""

        # Only make external API calls if needed
        if name in ['owner', 'description', 'created_at', 'public', 'files', 'filenames', 'repo']:
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
            _meta_url = 'http://gist.github.com/api/v1/json/%s' % (self.id)
            _meta = json.load(urllib.urlopen(_meta_url))['gists'][0]

        self.url = 'http://github.com/%s' % (self.id)
        self.embed_url = 'http://github.com/%s.js' % (self.id)
        self.epic_embed_url = 'http://github.com/%s.pibb' % (self.id)
        self.json_url = 'http://github.com/%s.json' % (self.id)

        for key, value in _meta.iteritems():

            if key == 'files':
                # Remap file key from API
                setattr(self, 'filenames', value)
            elif key == 'public':
                # Attach booleans
                setattr(self, key, value)
            elif key == 'created_at':
                # Attach datetime
                setattr(self, key, dtime(value))

            else:
                # Attach properties to object
                setattr(self, key, unicode(value))

        return _meta

    @property
    def files(self):
        """Fetches a gists files and stores them in the 'files' property"""
        _files = {}

        for fn in self.filenames:
            # Grab file contents
            _file_url = 'http://gist.github.com/raw/%s/%s' % (self.id, fn)
            _files[fn] = unicode(urllib.urlopen(_file_url).read())

        return _files


class Gists(object):
    """Gist API wrapper"""

    def __init__(self, username=None, token=None):
        # Token-based Authentication is unnecesary, gist api still in alpha
        self._username = username
        self._token = token

    @staticmethod
    def fetch_by_user(name):
        """Returns a set of public Gist objects owned by the given GitHub username"""

        _url = 'http://gist.github.com/api/v1/json/gists/%s' % (name)

        # Return a list of Gist objects
        return [Gist(json=g) for g in json.load(urllib.urlopen(_url))['gists']]


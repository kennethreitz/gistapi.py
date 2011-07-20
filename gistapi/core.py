# -*- coding: utf-8 -*-

"""
GistAPI.py -- A Python wrapper for GitHub's Gist API
(c) 2011 Kenneth Reitz. MIT License.

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

>>> Gists.fetch_by_user('kennethreitz')[-1].description
u'My .bashrc configuration'

>>> Gist(885658).comments[0].body
u'Great Stuff.'
"""


import cStringIO
import os.path

import requests
import urllib2
from datetime import datetime
import iso8601

try:
    import simplejson as json
except ImportError:
    import json

__all__ = ['Gist', 'Gists']

# Set your own credentials
USERNAME = 'YOUR GITHUB USERNAME'
TOKEN = 'YOUR GITHUB TOKEN'

GIST_BASE = 'http://gist.github.com/%s'
GIST_JSON = GIST_BASE % 'api/v1/json/%s'
API_BASE = 'https://api.github.com/%s'
API_GIST = API_BASE % 'gists%s'

class Gist(object):
    """Gist Object"""

    def __init__(self, id=None, json=None, username=None, token=None):
        self.id = id
        self._json = json
        self._username = username
        self._token = token

        # Map given repo id to gist id if none exists
        if self._json:
            self.id = json['repo'] if json.has_key('repo') else json['id']

        self.url = url = GIST_BASE % self.id
        self.embed_url = url + '.js'
        self.epic_embed_url = url + '.pibb'
        self.json_url = url + '.json'
        self.post_url = GIST_BASE % 'gists/%s' % self.id
    
    def __repr__(self):
        return '<gist %s>' % self.id

    def __getattribute__(self, name):
        """Get attributes, but only if needed."""

        # Only make external API calls if needed
        if name in ('owner', 'description', 'created_at', 'public',
                    'files', 'filenames', 'repo', 'comments', 'git_pull_url', 'git_push_url', 'forks', 'histories', 'user'):
            if not hasattr(self, '_meta'):
                self._meta = self._get_meta()

        return object.__getattribute__(self, name)

    def _get_meta(self):
        """Fetch Gist metadata."""

        # Use json data provided if available
        if self._json:
            _meta = self._json
            setattr(self, 'id', _meta['repo'] if _meta.has_key('repo') else _meta['id'])
        else:
            # Fetch Gist metadata
            _meta_url = GIST_JSON % self.id
            _meta = json.loads(requests.get(_meta_url).content)['gists'][0]

        for key, value in _meta.iteritems():

            if key == 'files':
                # Remap file key from API.
                setattr(self, 'filenames', value)
                # Store the {current_name: original_name} mapping.
                setattr(self, '_renames', dict((fn, fn) for fn in value))
            elif key == 'public':
                # Attach booleans
                setattr(self, key, value)
            elif key == 'created_at':
                # Attach datetime
                setattr(self, 'created_at', iso8601.parse_date(value))
            elif key == 'user':
                setattr(self, 'user', value)
            elif key == 'forks':
                forks = [GistFork.from_api(f) for f in value]
                setattr(self, 'forks', forks)
            elif key == 'history':
                histories = [GistHistory.from_api(h) for h in value]
                setattr(self, 'histories', histories)
            else:
                # Attach properties to object
                setattr(self, key, unicode(value))

        return _meta

    def _post(self, params, headers={}):
        """POST to the web form (internal method)."""
        r = requests.post(self.post_url, params, headers=self._)

        return r.status_code, r.content

    def reset(self):
        """Clear the local cache."""
        if hasattr(self, '_files'):
            del self._files
        if hasattr(self, '_meta'):
            del self._meta

    def auth(self, username, token):
        """Set credentials."""
        self._username = username
        self._token = token

    def rename(self, from_name, to_name):
        """Rename a file."""
        if from_name not in self.files:
            raise KeyError('File %r does not exist' % from_name)
        if to_name in self.files:
            raise KeyError('File %r already exist' % to_name)
        self.files[to_name] = self.files.pop(from_name)
        try:
            self._renames[to_name] = self._renames.pop(from_name)
        except KeyError:
            # New file
            pass

    def save(self):
        """Upload the changes to Github."""
        params = {
            '_method': 'put',
            'login': self._username or USERNAME,
            'token': self._token or TOKEN,
        }
        names_map = self._renames
        original_names = names_map.values()
        index = len(original_names)
        for fn, content in self.files.items():
            ext = os.path.splitext(fn)[1] or '.txt'
            try:
                orig = names_map.pop(fn)
            except KeyError:
                # Find a unique filename
                while True:
                    orig = 'gistfile%s' % index
                    index += 1
                    if orig not in original_names:
                        break
            params.update({
                'file_name[%s]' % orig: fn,
                'file_ext[%s]' % orig: ext,
                'file_contents[%s]' % orig: content,
            })
        code, msg = self._post(params=params)
        if code == 200:  # OK
            # If successful, clear the cache
            self.reset()
        return code, msg

    @property
    def files(self):
        """Fetch Gist's files and store them in the 'files' property."""
        try:
            return self._files
        except AttributeError:
            self._files = _files = {}

        for fn in self._meta['files']:
            # Grab file contents
            _file_url = GIST_BASE % 'raw/%s/%s' % (self.id, urllib2.quote(fn))
            _files[fn] = cStringIO.StringIO()
            _files[fn].write(requests.get(_file_url).content)

        return _files


class Gists(object):
    """Gist API wrapper"""

    def __init__(self, username=None, token=None):
        # Token-based Authentication is unnecessary, gist api still in alpha
        self._username = username
        self._token = token

    @staticmethod
    def fetch_by_user(name):
        """Return a list of public Gist objects owned by
        the given GitHub username."""

        _url = API_BASE % 'gists/%s' % name

        # Return a list of Gist objects
        return [Gist(json=g)
                for g in json.loads(requests.get(_url).content)]

    def fetch_gists(self, gist_id=None, options=None, public=False, starred=False):
        """Return a list of Gists. Required authorication"""
        if self._check_auth():
            _url = API_GIST % ''
            if gist_id:
                _url = API_GIST % '/' + str(gist_id)
                return Gist( json = json.loads(requests.get(_url, self._params(options)).content) )
            elif public:
                _url = API_GIST % '/public'
            elif starred:
                _url = API_GIST % '/starred'
            
            return [Gist(json=g)
                for g in json.loads(requests.get(_url, self._params(options), self._headers()).content)]
        else:
            return []
    
    def create_gist(self, files, description=None, public=True):
        """Create a Gist. Required authorication"""
        if self._check_auth():
            _url = API_GIST % ''
            options = {
                        'files': files,
                        'public': public
                       }
            if description is not None: options['description'] = description
            return Gist(json=json.loads(requests.post(_url, self._params2json(options), headers=self._headers()).content))
        else:
            return None

    def update_gist(self, gist_id, files=None, description=None):
        """Update a Gist. Required authorication"""
        if self._check_auth() and files is not None or description is not None:
            _url = API_GIST % '/' + str(gist_id)
            options = {}
            if files is not None: options['files'] = files
            if description is not None: options['description'] = description
#            return Gist( json = json.loads(requests.patch(_url, self._params2json(options), headers=self._headers()).content) )
            return requests.patch(_url, self._params2json(options), headers=self._headers())
        else:
            return None
    
    def delete_gist(self, gist_id):
        """Delete a Gist. Required authorication"""
        if self._check_auth():
            _url = API_GIST % '/' + str(gist_id)
            r = requests.delete(_url, headers=self._headers())
            return r.status_code == 204
        else:
            return False
    
    def star_gist(self, gist_id):
        """Star a Gist. Required authorication"""
        if self._check_auth():
            _url = API_GIST % '/' + str(gist_id) + '/star'
            r = requests.put(_url, headers=self._headers())
            return r.status_code == 204
        else:
            return False

    def unstar_gist(self, gist_id):
        """Unstar a Gist. Required authorication"""
        if self._check_auth():
            _url = API_GIST % '/' + str(gist_id) + '/star'
            r = requests.delete(_url, self._params(), headers=self._headers())
            return r.status_code == 204
        else:
            return False

    def check_starred(self, gist_id):
        """Check if a Gist is starred. Required authorication"""
        if self._check_auth():
            _url = API_GIST % '/' + str(gist_id) + '/star'
            r = requests.get(_url, self._params(), headers=self._headers())
            return r.status_code == 204
        else:
            return False
    
    def fork_gist(self, gist_id):
        """fork a Gist is starred. Required authorication"""
        if self._check_auth():
            _url = API_GIST % '/' + str(gist_id) + '/fork'
            return Gist( json = json.loads(requests.post(_url, self._params(), headers=self._headers()).content) )
        else:
            return None
    
    def fetch_comments(self, gist_id=None, comment_id=None, options=None):
        """Return a list of Gist Comments. Required authorication"""
        if self._check_auth():
            _url = API_GIST % '/' + str(gist_id) + 'comments'
            if comment_id:
                _url = API_GIST % '/comments/' + str(comment_id)
                
            gc = GistComment()
            return [gc.from_api(c)
                for c in json.loads(requests.get(_url, self._params(options)).content)]
        else:
            return []
    
    def create_comment(self, gist_id, body):
        """Create a Gist Comments. Required authorication"""
        if self._check_auth():
            _url = API_GIST % '/' + str(gist_id) + '/comments'
            return GistComment().from_api( json.loads( requests.post(_url, self._params2json({'body': body}), headers=self._headers()).content ) )
        else:
            return None
    
    def update_comment(self, comment_id, body):
        """Update a Gist Comments. Required authorication"""
        if self._check_auth():
            _url = API_GIST % '/comments/' + str(comment_id)
            return GistComment().from_api( json.loads( requests.patch(_url, self._params2json({'body': body}), headers=self._headers()).content ) )
        else:
            return None
    
    def delete_comment(self, comment_id):
        """Delete a Gist Comments. Required authorication"""
        if self._check_auth():
            _url = API_GIST % '/comments/' + str(comment_id)
            r = requests.delete(_url, headers=self._headers())
            return r.status_code == 204
        else:
            return False
    
    def _check_auth(self):
        return self._username and self._token
    
    def _params(self, params=None):
        return dict({
        }, **params or {})

    def _params2json(self, params=None):
        return json.dumps(dict({
        }, **params or {}))

    def _headers(self, headers=None):
        return dict({
            'authorization': 'token ' + self._token or TOKEN
        }, **headers or {})

class GistComment(object):
    """Gist comments."""
    
    def __init__(self): 
        self.body = None
        self.created_at = None
        self.gravatar_id = None
        self.id = None
        self.updated_at = None
        self.user = None

    def __repr__(self):
        return '<gist-comment %s>' % self.id

    @staticmethod
    def from_api(jsondict):
        """Returns new instance of GistComment containing given api dict."""
        comment = GistComment()
        
        comment.body = jsondict.get('body', None)
        comment.created_at = iso8601.parse_date(jsondict.get('created_at'))
        comment.gravatar_id = jsondict.get('gravatar_id', None)
        comment.id = jsondict.get('id', None)
        comment.updated_at = iso8601.parse_date(jsondict.get('updated_at'))
        comment.user = jsondict.get('user', None)
        
        return comment
        
class GistFork(object):
    """Gist forks"""
    
    def __init__(self): 
        self.user = None
        self.url = None
        self.created_at = None

    def __repr__(self):
        return '<gist-fork %s>' % self.url
    
    @staticmethod
    def from_api(jsondict):
        """Returns new instance of GistFork containing given api dict."""
        fork = GistFork()
        
        fork.user = jsondict.get('user', None)
        fork.url = jsondict.get('url', None)
        fork.created_at = iso8601.parse_date(jsondict.get('created_at'))
        
        return fork
    
class GistHistory(object):
    """Gist histories"""
    
    def __init__(self): 
        self.url = None
        self.version = None
        self.user = None
        self.change_status = None
        self.commited_at = None
        
    def __repr__(self):
        return '<gist-history %s>' % self.url
        
    @staticmethod
    def from_api(jsondict):
        """Returns new instance of GistFork containing given api dict."""
        fork = GistHistory()
        
        fork.url = jsondict.get('url', None)
        fork.version = jsondict.get('version', None)
        fork.user = jsondict.get('user', None)
        fork.change_status = jsondict.get('change_status', None)
        fork.committed_at = iso8601.parse_date(jsondict.get('committed_at'))
        
        return fork

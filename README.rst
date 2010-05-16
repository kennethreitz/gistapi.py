GistAPI.py
==========

This is a Python wrapper for GitHub's Gist API.

http://develop.github.com/p/gist.html

Example Usage
-------------

::

    from gistapi import *

    gist = Gist('d4507e882a07ac6f9f92')
    gist.description   # 'Example Gist for gist.py'

    gist.created_at    # '2010/05/16 10:51:15 -0700'
    gist.public        # False
    gist.filenames     # ['exampleEmptyFile', 'exampleFile']
    gist.files         # {'exampleFile': 'Example file content.', 'exampleEmptyFile': ''} 

    Gists.fetch_by_user('kennethreitz')[-1].description    # 'My .bashrc configuration'

Installation
------------

	pip install gistapi
	
Or, if you must: 

	easy_install gistapi
	

Roadmap
-------

* Implement Gist API methods as they are introduced
	- Token based Authentication
	- Listing your private Gists
	- Create a new Gist
	- Fork a Gist
	- Delete a Gist
	- Edit a Gist
* Possibly use other hacks in the meantime
	- Gist's New Gist method? (Post to web form?)
* Possibly add command line gist interface


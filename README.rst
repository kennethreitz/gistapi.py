GistAPI.py
==========

This is a Python wrapper for GitHub's Gist API.

http://develop.github.com/p/gist.html

Example Usage
-------------
	from gistapi import *  

	>> Gist('d4507e882a07ac6f9f92').repo  
	'd4507e882a07ac6f9f92'

	>> Gist('d4507e882a07ac6f9f92').description  
	'Example Gist for gist.py'

	>> Gist('d4507e882a07ac6f9f92').created_at  
	'2010/05/16 10:51:15 -0700'

	>> Gist('d4507e882a07ac6f9f92').public  
	False

	>> Gist('d4507e882a07ac6f9f92').filenames  
	['exampleEmptyFile', 'exampleFile']

	>> Gist('d4507e882a07ac6f9f92').files  
	{'exampleFile': 'Example file content.', 'exampleEmptyFile': ''}  

	>> Gists.fetch_by_user('kennethreitz')[-1].description  
	'My .bashrc configuration'

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
* Possibly add command line gist interface


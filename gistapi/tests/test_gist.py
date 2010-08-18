from gistapi import *

for gist in Gists.fetch_by_user('defunkt'):
    if gist.description == 'A list of Gist clients.':
        print gist.id
        print gist.repo
        print gist.embed_url

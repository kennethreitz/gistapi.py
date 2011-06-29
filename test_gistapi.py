#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

import gistapi
from gistapi import Gist, Gists


class RequestsTestSuite(unittest.TestCase):
    """Requests test cases."""

    def setUp(self):
        username = ''
        token = ''
        self.api = Gists(username=username, token=token)

    def tearDown(self):
        """Teardown."""
        pass

    def test_repo_fetch(self):
        r1 = Gist('d4507e882a07ac6f9f92').repo
        r2 = u'd4507e882a07ac6f9f92'

        self.assertEqual(r1, r2)

    def test_owner_fetch(self):
        r1 = Gist('d4507e882a07ac6f9f92').owner
        r2 = u'kennethreitz'

        self.assertEqual(r1, r2)

    def test_created_at_fetch(self):
        r1 = Gist('d4507e882a07ac6f9f92').created_at.isoformat()
        r2 = '2010-05-16T10:51:15'

        self.assertEqual(r1, r2)

    def test_public_fetch(self):
        r1 = Gist('d4507e882a07ac6f9f92').public
        r2 = False

        self.assertEqual(r1, r2)

    def test_fetch_filesnames(self):
        r1 = Gist('d4507e882a07ac6f9f92').filenames
        r2 = ['exampleEmptyFile', 'exampleFile']

        self.assertEqual(r1, r2)

    def test_gist_search(self):
        r1 = Gists.fetch_by_user('kennethreitz')[-1].description
        r2 = u'My .bashrc configuration'

        self.assertEqual(r1, r2)

    def test_gist_comments(self):
        r1 = Gist(885658).comments[0].body
        r2 = u'Great stuff.'

        self.assertEqual(r1, r2)
    
    def test_fetch_gists(self):
        actual = self.api.fetch_gists()
        self.assertEqual(actual is not None, True)
    
    def test_fetch_gists_no_auth(self):
        pass
    
    def test_create_gist(self):
        files = {
                 'test1.txt': {
                           'content': 'test1'
                           },
                 'test2.txt': {
                           'content': 'test2'
                           },
                 }
        description = 'API v3 TEST'
        public = True
#        actual = self.api.create_gist(files, description, public)
#        self.assertEqual(actual, True)
    
    def test_update_gist(self):
        gist_id = '1053195'
        files = {
                 'test1.txt': {
                           'content': 'test1 update'
                           },
                 'test2.txt': {
                           'content': 'test2 update'
                           },
                 }
        description = 'API v3 TEST update'
#        g = self.api.update_gist(gist_id, files, description)
    
    def test_delete_gist(self):
        gist_id = '1053195'
#        actual = self.api.delete_gist(gist_id)
#        self.assertEqual(actual, True)

        pass
    
    def test_star_gist(self):
        gist_id = '1053253'
#        actual = self.api.star_gist(gist_id)
#        self.assertEqual(actual, True)
    
    def test_unstar_gist(self):
        gist_id = '1053253'
#        self.api.star_gist(gist_id)
#        actual = self.api.unstar_gist(gist_id)
#        self.assertEqual(actual, True)
    
    def test_check_starred(self):
        gist_id = '1053253'
#        self.api.star_gist(gist_id)
#        actual = self.api.check_starred(gist_id)
#        self.assertEqual(actual, True)
    
    def test_fork_gist(self):
        gist_id = '1046788'
#        actual = self.api.fork_gist(gist_id)
#        self.assertEqual(actual, True)
    
    def test_fetch_comments(self):
        pass
    
    def test_create_comment(self):
        gist_id = '1053253'
        body = 'test1 from api.'
#        actual = self.api.create_comment(gist_id, body)
#        self.assertEqual(actual.body, body)
    
    def test_update_comment(self):
#        comment_id = '38016'
        body = 'test1 from api update.'
#        actual = self.api.update_comment(comment_id, body)
#        self.assertEqual(actual.body, body)
    
    def test_delete_comment(self):
        comment_id = '38016'
#        actual = self.api.delete_comment(comment_id)
#        self.assertEqual(actual, True)

if __name__ == '__main__':
    unittest.main()

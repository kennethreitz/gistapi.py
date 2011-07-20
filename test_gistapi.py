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
        self.assertEqual(len(actual) > 0, True)

    def _create_dummy_gist(self):
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
        return self.api.create_gist(files, description, public)
    
    def _create_dummy_comment(self, gist_id):
        body = 'test1 from api.'
        return self.api.create_comment(gist_id, body)
        
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
        actual = self.api.create_gist(files, description, public)
        
        self.assertEqual(actual.owner, self.api._username)
        self.assertEqual(actual.description, description)
        self.assertEqual(len(actual.files), len(files))
        
        self.api.delete_gist(actual.id)
    
    def test_update_gist(self):
        g = self._create_dummy_gist()
        files = {
                 'test1.txt': {
                           'content': 'test1 update'
                           },
                 'test2.txt': {
                           'content': 'test2 update'
                           },
                 }
        description = 'API v3 TEST update'
        actual = self.api.update_gist(g.id, files, description)
        
        self.assertEqual(actual.owner, self.api._username)
        self.assertEqual(actual.description, description)
        
        self.api.delete_gist(g.id)
    
    def test_delete_gist(self):
        g = self._create_dummy_gist()
        actual = self.api.delete_gist(g.id)
        
        self.assertEqual(actual, True)
    
    def test_star_gist(self):
        g = self._create_dummy_gist()
        actual = self.api.star_gist(g.id)
        
        self.assertEqual(actual, True)
        
        self.api.unstar_gist(g.id)
        self.api.delete_gist(g.id)
    
    def test_unstar_gist(self):
        g = self._create_dummy_gist()
        self.api.star_gist(g.id)
        actual = self.api.unstar_gist(g.id)
        
        self.assertEqual(actual, True)
        
        self.api.delete_gist(g.id)
    
    def test_check_starred_checked(self):
        g = self._create_dummy_gist()
        self.api.star_gist(g.id)
        actual = self.api.check_starred(g.id)
        
        self.assertEqual(actual, True)

        self.api.delete_gist(g.id)
    
    def test_check_starred_no_checked(self):
        g = self._create_dummy_gist()
        actual = self.api.check_starred(g.id)
        
        self.assertEqual(actual, False)
        
        self.api.delete_gist(g.id)
    
    def test_fork_gist(self):
        gist_id = '1'
        g = self.api.fetch_gists(gist_id=gist_id)
        actual = self.api.fork_gist(gist_id)
        
        self.assertEqual(actual.description, g.description)
        #TODO check actual in g.forks
    
    def test_fetch_comments(self):
        g = self._create_dummy_gist()
        self._create_dummy_comment(g.id)
        actual = self.api.fetch_comments(g.id)
        self.assertEqual(len(actual), 1)
        
        for c in actual:
            self.api.delete_comment(c.id)
        self.api.delete_gist(g.id)
    
    def test_create_comment(self):
        g = self._create_dummy_gist()
        body = 'test1 from api.'
        actual = self.api.create_comment(g.id, body)
        
        self.assertEqual(actual.body, body)
        
        self.api.delete_gist(g.id)
    
    def test_update_comment(self):
        g = self._create_dummy_gist()
        c = self._create_dummy_comment(g.id)
        body = 'test1 from api update.'
        actual = self.api.update_comment(c.id, body)
        
        self.assertEqual(actual.body, body)
        
        self.api.delete_comment(c.id)
        self.api.delete_gist(g.id)
    
    def test_delete_comment(self):
        g = self._create_dummy_gist()
        c = self._create_dummy_comment(g.id)
        actual = self.api.delete_comment(c.id)
        
        self.assertEqual(actual, True)
        
        self.api.delete_gist(g.id)

if __name__ == '__main__':
    unittest.main()

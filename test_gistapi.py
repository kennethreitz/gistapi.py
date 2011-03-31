#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

import gistapi
from gistapi import Gist, Gists


class RequestsTestSuite(unittest.TestCase):
    """Requests test cases."""

    def setUp(self):
        pass

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
    


if __name__ == '__main__':
    unittest.main()

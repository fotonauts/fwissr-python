#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_fwissr
----------------------------------

Tests for `fwissr` module.
"""

import unittest

from fwissr.fwissr import Fwissr

from test_helpers import *

class TestFwissr(unittest.TestCase):
    def setUp(self):
        Fwissr.main_conf_path = tmp_conf_dir()
        delete_tmp_conf_files()
        delete_tmp_mongo_db()

    def test_manager_global_registry(self):
        setup_global_conf()
        self.assertEqual( Fwissr['/foo'], 'bar')
        self.assertEqual( Fwissr['/bar'], 'baz')
        self.assertEqual( Fwissr['/cam'], { 'en': { 'bert': { 'pim': { 'pam': [ 'pom', 'pum' ] } } } })
        self.assertEqual( Fwissr['/cam/en'], { 'bert': { 'pim': { 'pam': [ 'pom', 'pum' ] } } })
        self.assertEqual( Fwissr['/cam/en/bert'], { 'pim': { 'pam': [ 'pom', 'pum' ] } })
        self.assertEqual( Fwissr['/cam/en/bert/pim'], { 'pam': [ 'pom', 'pum' ] })
        self.assertEqual( Fwissr['/cam/en/bert/pim/pam'], [ 'pom', 'pum' ])
        self.assertEqual( Fwissr['/gein'], 'gembre')
        self.assertEqual( Fwissr['/mouarf'], { 'lol': { 'meu': 'ringue', 'pa': { 'pri': 'ka'} } })
        self.assertEqual( Fwissr['/mouarf/lol'], { 'meu': 'ringue', 'pa': { 'pri': 'ka'} })
        self.assertEqual( Fwissr['/mouarf/lol/meu'], 'ringue')
        self.assertEqual( Fwissr['/mouarf/lol/pa'], { 'pri': 'ka'})
        self.assertEqual( Fwissr['/mouarf/lol/pa/pri'], 'ka')
        self.assertEqual( Fwissr['/pa'], { 'ta': 'teu'})
        self.assertEqual( Fwissr['/pa/ta'], 'teu')

    def test_no_leading_slash_is_ok(self):
        setup_global_conf()

        self.assertEqual( Fwissr['foo'], 'bar')
        self.assertEqual( Fwissr['cam'], { 'en': { 'bert': { 'pim': { 'pam': [ 'pom', 'pum' ] } } } })
        self.assertEqual( Fwissr['cam/en/bert/pim/pam'], [ 'pom', 'pum' ])

if __name__ == '__main__':
    unittest.main()

#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_fwissr
----------------------------------

Tests for `fwissr` module.
"""

import unittest
from test_helpers import *
import fwissr
import Fwissr

class TestFwissr(unittest.TestCase):

    @classmethod
    def setupClass(cls):
        fwissr.main_conf_path = tmp_conf_dir()

    def setUp(self):
        delete_tmp_conf_file()
        delete_tmp_mongo_db()

    def test_manager_global_registry(self):
        setup_global_conf()
        self.assertEqual(Fwissr['/foo'], 'bar')


if __name__ == '__main__':
    unittest.main()

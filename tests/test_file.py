#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_fwissr
----------------------------------

Tests for `fwissr` module.
"""

import unittest
import time

from fwissr.source.file import File

from test_helpers import *

class TestFwissr(unittest.TestCase):
        def setUp(self):
                delete_tmp_conf_files()

        def test_instanciate(self):
            create_tmp_conf_file('test.json', {})
            source = File(tmp_conf_file('test.json'))

            self.assertEqual(source.__class__, File)
            self.assertEqual(source.path, tmp_conf_file('test.json'))

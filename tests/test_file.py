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


        def test_conf1(self, filename = None):
            test_conf = {
                'foo': 'bar',
                'cam': { 'en': 'bert'},
            }
            if filename is not None:
                create_tmp_conf_file(filename, test_conf)
            return test_conf

        def test_instanciate(self):
            create_tmp_conf_file('test.json', {})
            source = File(tmp_conf_file('test.json'))

            self.assertEqual(source.__class__, File)
            self.assertEqual(source.path, tmp_conf_file('test.json'))

        def test_raises_if_not_exists(self):
            with self.assertRaises(Exception):
                File(tmp_conf_file('pouet.json'))

        def test_fetches_json_conf(self):
            # create conf file
            test_conf = self.test_conf1('test.json')

            # test
            source = File.from_path(tmp_conf_file('test.json'))
            conf_fetched = source.fetch_conf()

            # check
            self.assertEqual(conf_fetched, { 'test': test_conf })

        def test_fetches_yaml_conf(self):
            # create conf file
            test_conf = self.test_conf1('test.yml')

            # test
            source = File.from_path(tmp_conf_file('test.yml'))
            conf_fetched = source.fetch_conf()

            # check
            self.assertEqual(conf_fetched, { 'test': test_conf })

        def test_fetches_all_from_directory(self):
            test1_conf = self.test_conf1('test1.json')

            test2_conf = {
                'jean': 'bon',
                'terieur': [ 'alain', 'alex' ]
            }
            create_tmp_conf_file('test2.yml', test2_conf)


            # test
            source = File.from_path(tmp_conf_dir())
            conf_fetched = source.fetch_conf()

            # check
            self.assertEqual(conf_fetched, { 'test1': test1_conf, 'test2': test2_conf })

        def test_maps_filename_to_key_parts(self):
            test_conf = self.test_conf1('test.with.parts.json')

            source = File.from_path(tmp_conf_file('test.with.parts.json'))
            conf_fetched = source.fetch_conf()
            self.assertEqual(conf_fetched, { 'test': { 'with': { 'parts': test_conf }}})

        def test_no_filename_map_when_toplevel(self):
            top_level_conf_file_name = "%s.json" % File.TOP_LEVEL_CONF_FILES[0]
            test_conf = self.test_conf1(top_level_conf_file_name)

            # test
            source = File.from_path(tmp_conf_file(top_level_conf_file_name))
            conf_fetched = source.fetch_conf()

            # check
            self.assertEqual(conf_fetched, test_conf)

        def test_no_filename_map_custom_toplevel(self):
            test_conf = self.test_conf1("test.json")

            source = File.from_path(tmp_conf_file("test.json"), {"top_level" : True})
            conf_fetched = source.fetch_conf()

            self.assertEqual(conf_fetched, test_conf)

        def test_refresh_if_allowed(self):
            test_conf = self.test_conf1("test.json")
            source = File.from_path(tmp_conf_file("test.json"), {"refresh" : True})

            conf_fetched = source.get_conf()
            self.assertEqual(conf_fetched, { 'test': test_conf })

            # Change file
            delete_tmp_conf_files()
            test_conf_modified = {
              'foo': 'pouet',
              'cam': { 'en': 'bert'},
            }
            create_tmp_conf_file("test.json", test_conf_modified)

            # Test
            conf_fetched = source.get_conf()
            self.assertEqual(conf_fetched, { 'test': test_conf_modified })

        def test_NO_refresh_if_NOT_allowed(self):
            test_conf = self.test_conf1("test.json")
            source = File.from_path(tmp_conf_file("test.json"))

            conf_fetched = source.get_conf()
            self.assertEqual(conf_fetched, { 'test': test_conf })

            # Change file
            delete_tmp_conf_files()
            test_conf_modified = {
              'foo': 'pouet',
              'cam': { 'en': 'bert'},
            }
            create_tmp_conf_file("test.json", test_conf_modified)

            # Test
            conf_fetched = source.get_conf()
            self.assertEqual(conf_fetched, { 'test': test_conf })

        def test_reset(self):
            test_conf = self.test_conf1("test.json")

            # test
            source = File.from_path(tmp_conf_file('test.json'))
            conf_fetched = source.get_conf()

            # check
            self.assertEqual(conf_fetched, { 'test': test_conf })

            # Change file
            delete_tmp_conf_files()
            test_conf_modified = {
              'foo': 'pouet',
              'cam': { 'en': 'bert'},
            }
            create_tmp_conf_file("test.json", test_conf_modified)

            self.assertEqual(source.get_conf(), { 'test': test_conf })
            source.reset()
            self.assertEqual(source.get_conf(), { 'test': test_conf_modified })


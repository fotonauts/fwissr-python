#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_fwissr
----------------------------------

Tests for `fwissr` module.
"""

import unittest
import time

from fwissr.registry import Registry
from fwissr.source.file import File
from fwissr.fwissr import Fwissr

from test_helpers import tmp_conf_dir, delete_tmp_conf_files, \
    create_tmp_conf_file, tmp_conf_file


class TestFwissr(unittest.TestCase):
    def setUp(self):
        Fwissr.main_conf_path = tmp_conf_dir()
        delete_tmp_conf_files()

    def test_create_source(self):
        test_conf = {'foo': 'bar', 'cam': {'en': 'bert'}}
        create_tmp_conf_file("test.json", test_conf)

        registry = Registry(refresh_period=20)
        registry.add_source(File(tmp_conf_file('test.json')))

        self.assertEqual(registry.refresh_period, 20)
        self.assertEqual(registry['/test/foo'], 'bar')
        self.assertEqual(registry['/test/cam/en'], 'bert')
        self.assertEqual(registry['/test/cam'], {'en': 'bert'})

        self.assertEqual(registry['/meuh'], None)
        self.assertEqual(registry['/test/meuh'], None)
        self.assertEqual(registry['/test/cam/meuh'], None)

    def test_default_refresh_period(self):
        registry = Registry()
        self.assertEqual(
            registry.refresh_period,
            Registry.DEFAULT_REFRESH_PERIOD)

    def test_instanciate_with_several_sources(self):
        test_conf = {
            'foo': 'bar',
            'cam': {'en': 'bert'},
        }
        create_tmp_conf_file('test.json', test_conf)

        test_conf = {
            'foo': 'baz',
            'cam': {'et': 'rat'},
            'jean': 'bon',
        }
        create_tmp_conf_file('test2.json', test_conf)

        registry = Registry()
        registry.add_source(
            File(tmp_conf_file('test.json'), {'top_level': True}))

        self.assertEqual(registry['/foo'], 'bar')
        self.assertEqual(registry['/cam'], {'en': 'bert'})
        self.assertEqual(registry['/cam/en'], 'bert')

        registry.add_source(
            File(tmp_conf_file('test2.json'), {'top_level': True}))

        self.assertEqual(registry['/foo'], 'baz')
        self.assertEqual(registry['/cam'], {'en': 'bert', 'et': 'rat'})
        self.assertEqual(registry['/cam/en'], 'bert')
        self.assertEqual(registry['/cam/et'], 'rat')
        self.assertEqual(registry['/jean'], 'bon')

    def test_list_keys(self):
        test_conf = {
            'foo': 'bar',
            'jean': ['bon', 'rage'],
            'cam': {'en': {'bert': 'coulant'}},
        }
        create_tmp_conf_file('test.json', test_conf)

        registry = Registry()
        registry.add_source(File(tmp_conf_file('test.json')))

        self.assertEqual(registry.keys(), [
            '/test',
            '/test/cam',
            '/test/cam/en',
            '/test/cam/en/bert',
            '/test/foo',
            '/test/jean',
        ])

    def test_dump(self):
        # create conf file
        test_conf = {
            'foo': 'bar',
            'jean': ['bon', 'rage'],
            'cam': {'en': {'bert': 'coulant'}},
        }
        create_tmp_conf_file('test.json', test_conf)

        registry = Registry()
        registry.add_source(File(tmp_conf_file('test.json')))

        # test
        self.assertEqual(registry.dump(), {'test': test_conf})

    def test_get_slash(self):
        # create conf file
        test_conf = {
            'foo': 'bar',
            'jean': ['bon', 'rage'],
            'cam': {'en': {'bert': 'coulant'}},
        }
        create_tmp_conf_file('test.json', test_conf)

        registry = Registry()
        registry.add_source(File(
            tmp_conf_file('test.json'),
            {"top_level": True}))

        # test
        self.assertEqual(registry.get("/"), test_conf)

    def test_not_refresh_thread(self):
        # create conf file
        test_conf = {
            'foo': 'bar',
            'cam': {'en': 'bert'},
        }
        create_tmp_conf_file('test.json', test_conf)

        registry = Registry(refresh_period=5)
        registry.add_source(
            File(tmp_conf_file('test.json'), {'refresh': True}))

        # check
        self.assertTrue(registry.refresh_thread is not None)
        self.assertTrue(registry.refresh_thread.is_alive())

    def test_no_refresh_until_refresh_option(self):
        test_conf = {
            'foo': 'bar',
            'cam': {'en': 'bert'},
        }
        create_tmp_conf_file('test.json', test_conf)

        registry = Registry(refresh_period=3)
        registry.add_source(
            File(tmp_conf_file('test.json'), {'refresh': True}))
        self.assertEqual(registry.dump(), {'test': test_conf})

        # modify conf file
        delete_tmp_conf_files()

        test_conf_modified = {
            'pouet': 'meuh'
        }
        create_tmp_conf_file('test.json', test_conf_modified)

        time.sleep(1)

        # not refreshed yet
        self.assertEqual(registry.dump(), {'test': test_conf})

    def test_refresh_after_refresh_period(self):
        test_conf = {
            'foo': 'bar',
            'cam': {'en': 'bert'},
        }
        create_tmp_conf_file('test.json', test_conf)

        registry = Registry(refresh_period=1)
        registry.add_source(
            File(tmp_conf_file('test.json'), {'refresh': True}))

        self.assertEqual(registry.dump(), {'test': test_conf})

        # modify conf file
        delete_tmp_conf_files

        test_conf_modified = {
            'pouet': 'meuh',
        }
        create_tmp_conf_file('test.json', test_conf_modified)
        time.sleep(3)

        self.assertEqual(registry.dump(), {'test': test_conf_modified})

        # modify conf file
        delete_tmp_conf_files

        test_conf_modified_2 = {
            'pouet': 'tagada',
        }
        create_tmp_conf_file('test.json', test_conf_modified_2)

        time.sleep(3)

        # refresh done
        self.assertEqual(registry.dump(), {'test': test_conf_modified_2})

    def test_reloads(self):
        # create conf file
        test_conf = {
            'foo': 'bar',
            'jean': ['bon', 'rage'],
            'cam': {'en': {'bert': 'coulant'}},
        }
        create_tmp_conf_file('test.json', test_conf)

        registry = Registry()
        registry.add_source(File(tmp_conf_file('test.json')))
        self.assertEqual(registry.dump(), {'test': test_conf})

        # modify conf file
        delete_tmp_conf_files()

        test_conf_modified = {
            'pouet': 'meuh',
        }
        create_tmp_conf_file('test.json', test_conf_modified)

        # test
        self.assertEqual(registry.dump(), {'test': test_conf})
        registry.reload()
        self.assertEqual(registry.dump(), {'test': test_conf_modified})

    def test_frozen(self):
        test_conf = {
            'foo': 'bar',
            'cam': {'en': 'bert'},
        }
        create_tmp_conf_file('test.json', test_conf)

        test_conf = {
            'foo': 'baz',
            'cam': {'et': 'rat'},
            'jean': 'bon',
        }
        create_tmp_conf_file('test2.json', test_conf)
        registry = Registry()
        registry.add_source(File(
            tmp_conf_file('test.json'),
            {'top_level': True}))

        self.assertEqual(registry['/foo'], 'bar')
        self.assertTrue(registry.frozen)
        self.assertRaises(TypeError, setattr, registry['/cam'], '__setitem__', 'heu', 'lotte')


if __name__ == '__main__':
    unittest.main()

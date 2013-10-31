#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_mongo
----------------------------------

Tests for `fwissr` module.
"""

import unittest
import time

from fwissr.source.mongodb import Mongodb
from fwissr.source.source_factory import SourceFactory

from test_helpers import *

class TestFwissr(unittest.TestCase):
    def setUp(self):
        delete_tmp_mongo_db()

    def create_test_conf(self, colname = None):
            # create collection
        test_conf = {
            'foo': 'bar',
            'cam': { 'en': 'bert'},
        }
        if not colname is None:
            create_tmp_mongo_col(colname, test_conf)
        return test_conf


    def test_instanciate_from_uri(self):
        create_tmp_mongo_col('test', {})

        source = SourceFactory.from_settings({ 'mongodb' : tmp_mongo_db_uri(tmp_mongo_db()), 'collection': 'test'})

        self.assertEqual(source.__class__, Mongodb)
        self.assertEqual(source.db_name, tmp_mongo_db())
        self.assertEqual(source.collection_name, 'test')

    def test_fetches_conf(self):
        test_conf = self.create_test_conf('test')
        source =  SourceFactory.from_settings({ 'mongodb' : tmp_mongo_db_uri(tmp_mongo_db()), 'collection': 'test'})

        conf_fetched = source.fetch_conf()
        self.assertEqual(conf_fetched, { 'test': test_conf })

    def test_map_collection_names_to_key_pars(self):
        test_conf = self.create_test_conf('cam.en.bert')
        source =  SourceFactory.from_settings({ 'mongodb' : tmp_mongo_db_uri(tmp_mongo_db()), 'collection': 'cam.en.bert'})

        conf_fetched = source.fetch_conf()
        self.assertEqual(conf_fetched, { 'cam': { 'en': { 'bert': test_conf }}})

    def test_no_map_for_top_level(self):
        top_level_conf_col_name = Mongodb.TOP_LEVEL_COLLECTIONS[0]
        test_conf = self.create_test_conf(top_level_conf_col_name)
        source =  SourceFactory.from_settings({ 'mongodb' : tmp_mongo_db_uri(tmp_mongo_db()), 'collection': top_level_conf_col_name})

        conf_fetched = source.fetch_conf()
        self.assertEqual(conf_fetched, test_conf)

    def test_no_map_for_keyparts_for_top_level(self):
        test_conf = self.create_test_conf('cam.en.bert')
        source =  SourceFactory.from_settings({ 'mongodb' : tmp_mongo_db_uri(tmp_mongo_db()), 'collection': 'cam.en.bert', 'top_level' : True})

        conf_fetched = source.fetch_conf()
        self.assertEqual(conf_fetched, test_conf)

    def test_refresh_if_allowed(self):
        test_conf = self.create_test_conf('test')

        source =  SourceFactory.from_settings({ 'mongodb' : tmp_mongo_db_uri(tmp_mongo_db()), 'collection': 'test', 'refresh': True})

        conf_fetched = source.get_conf()
        self.assertEqual(conf_fetched, { 'test': test_conf })

        delete_tmp_mongo_db()

        test_conf_modified = {
            'foo': 'meuh'
        }
        create_tmp_mongo_col('test', test_conf_modified)
        conf_fetched = source.get_conf()
        self.assertEqual(conf_fetched, { 'test': test_conf_modified })

    def test_NO_refresh_when_NOT_allowed(self):
        test_conf = self.create_test_conf('test')

        source =  SourceFactory.from_settings({ 'mongodb' : tmp_mongo_db_uri(tmp_mongo_db()), 'collection': 'test'})

        conf_fetched = source.get_conf()
        self.assertEqual(conf_fetched, { 'test': test_conf })

        delete_tmp_mongo_db()

        test_conf_modified = {
            'foo': 'meuh'
        }
        create_tmp_mongo_col('test', test_conf_modified)
        conf_fetched = source.get_conf()
        self.assertEqual(conf_fetched, { 'test': test_conf })

    def test_reset(self):
        test_conf = self.create_test_conf('test')

        source =  SourceFactory.from_settings({ 'mongodb' : tmp_mongo_db_uri(tmp_mongo_db()), 'collection': 'test'})

        conf_fetched = source.get_conf()
        self.assertEqual(conf_fetched, { 'test': test_conf })

        delete_tmp_mongo_db()

        test_conf_modified = {
            'foo': 'meuh'
        }
        create_tmp_mongo_col('test', test_conf_modified)
        self.assertEqual(source.get_conf(), { 'test': test_conf })
        source.reset()
        self.assertEqual(source.get_conf(), { 'test': test_conf_modified })







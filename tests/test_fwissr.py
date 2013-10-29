#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_fwissr
----------------------------------

Tests for `fwissr` module.
"""

import unittest

from fwissr import fwissr

import pymongo
import os
import json
import yaml
import shutil

def setup_global_conf():
    # create additional file sources
    first = 'mouarf.lol.json'
    second = 'trop.mdr.json'


    create_tmp_conf_file(first, {
        'meu': 'ringue',
        'pa': { 'pri': 'ka'},
    })

    create_tmp_conf_file(second, {
        'gein': 'gembre',
        'pa': { 'ta': 'teu'},
    })

    # create additional mongodb sources
    create_tmp_mongo_col('roque.fort', {
        'bar': 'baz',
    })

    create_tmp_mongo_col('cam.en.bert', {
        'pim': { 'pam': [ 'pom', 'pum' ] },
    })

    # create main conf file
    fwissr_conf = {
        'fwissr_sources': [
            { 'filepath': tmp_conf_file(first) },
            { 'filepath': tmp_conf_file(second), 'top_level': true },
            { 'mongodb': tmp_mongo_db_uri, 'collection': 'roque.fort', 'top_level': true },
            { 'mongodb': tmp_mongo_db_uri, 'collection': 'cam.en.bert' },
        ],
        'fwissr_refresh_period': 5,
        'foo':'bar',
    }
    create_tmp_conf_file('fwissr.json', fwissr_conf)



def tmp_conf_dir():
    return "/tmp/fwissr.spec"

def tmp_conf_file(filename):
    return "%s/%s" % (tmp_conf_dir(), filename)

def create_tmp_conf_file(filename, conf):
    conf_file_path = os.path.join(tmp_conf_dir(), filename)

    if os.path.exists(conf_file_path):
        os.unlink(conf_file_path)

    if not os.path.lexists(tmp_conf_dir()):
        os.makedirs(tmp_conf_dir())

    f = open(conf_file_path, 'w')
    if os.path.splitext(filename)[1] == ".json":
        f.write(json.dumps(conf, sort_keys=True))
    elif os.path.splitext(filename)[1] == ".yml":
        f.write(yaml.dump(conf, Dumper=yaml.CDumper))
    else:
        raise Exception("Unsupported conf file type", filename)
    f.close()

def delete_tmp_conf_file():
    if os.path.abspath(tmp_conf_dir()) == os.path.abspath(Fwissr.DEFAULT_MAIN_CONF_PATH):
        raise Exception("Hey, don't delete all legal conf files !", tmp_conf_dir())
    shutil.rmtree(tmp_conf_dir(), True)

def set_tmp_conf(conf_dir = tmp_conf_dir, user_conf_dir = ""):
    Fwissr.conf_dir = conf_dir
    Fwissr.user_conf_dir = user_conf_dir


def tmp_mongo_hostname():
    return "localhost"

def tmp_mongo_port():
    return 27017

def tmp_mongo_db():
    return "fwissr_spec"

def tmp_mongo_db_uri():
    return "mongodb://%s:%s/%s" % (tmp_mongo_hostname(), tmp_mongo_port(), tmp_mongo_db())

def create_tmp_mongo_col(name, conf):
    pass

def delete_tmp_mongo_db():
    pass

class TestFwissr(unittest.TestCase):

    def setUp(self):
        create_tmp_conf_file("pouet.yml", {"salut mec": "ca va"})

    def test_something(self):
        pass

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
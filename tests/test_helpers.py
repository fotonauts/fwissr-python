

from pymongo import MongoClient
import os
import json
import yaml
import shutil
import locale

from fwissr.fwissr import Fwissr

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
            { 'filepath': tmp_conf_file(second), 'top_level': True },
            { 'mongodb': mongo_connection_url(tmp_mongo_db()), 'collection': 'roque.fort', 'top_level': True },
            { 'mongodb': mongo_connection_url(tmp_mongo_db()), 'collection': 'cam.en.bert' },
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

def delete_tmp_conf_files():
    if os.path.abspath(tmp_conf_dir()) == os.path.abspath(Fwissr.DEFAULT_MAIN_CONF_PATH):
        raise Exception("Hey, don't delete all legal conf files !", tmp_conf_dir())
    shutil.rmtree(tmp_conf_dir(), True)

def set_tmp_conf(conf_dir = tmp_conf_dir, user_conf_dir = ""):
    Fwissr.conf_dir = conf_dir
    Fwissr.user_conf_dir = user_conf_dir


def env_or(env_name, or_value):
    """Returns the env variable value or or_value if unset"""
    if env_name in os.environ:
        return os.environ[env_name]
    else:
        return or_value

def tmp_mongo_hostname():
    return env_or("MONGO_HOSTNAME", "localhost")

def tmp_mongo_port():
    return env_or("MONGO_PORT", 27017)
    if "MONGO_PORT" in os.environ:
        return locale.atoi(os.environ["MONGO_PORT"])
    else:
        return 27017

def tmp_mongo_db():
    return "fwissr_spec"

def tmp_mongo_db_uri(db = ""):
    return "mongodb://%s:%s/%s" % (tmp_mongo_hostname(),
        tmp_mongo_port(),
        db)

def mongo_connection():
    return MongoClient(tmp_mongo_db_uri())

def create_tmp_mongo_col(name, conf):
    col = mongo_connection()[tmp_mongo_db()].create_collection(name)
    for key, val in conf.iteritems():
        col.insert({'_id': key, 'value' : val})

def delete_tmp_mongo_db():
    client = mongo_connection()
    client.drop_database(tmp_mongo_db())


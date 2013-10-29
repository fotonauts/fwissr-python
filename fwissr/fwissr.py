#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os


class FwissrModule(object):
    # main conf file
    MAIN_CONF_FILE = "fwissr.json"
    # default path where main conf file is located
    DEFAULT_MAIN_CONF_PATH = "/etc/fwissr"
    # default directory (relative to current user's home) where user's main conf file is located
    DEFAULT_MAIN_USER_CONF_DIR = ".fwissr"

    def __init__(self):
        self._main_conf_path = self.DEFAULT_MAIN_CONF_PATH
        self._main_user_conf_path = os.path.join(self.find_home(), self.DEFAULT_MAIN_USER_CONF_DIR)

    def main_conf_path():
        doc = "The main_conf_path property."
        def fget(self):
            return self._main_conf_path
        def fset(self, value):
            self._main_conf_path = value
        return locals()
    main_conf_path = property(**main_conf_path())


    def main_user_conf_path():
        doc = "The main_user_conf_path property."
        def fget(self):
            return self._main_user_conf_path
        def fset(self, value):
            self._main_user_conf_path = value
        return locals()
    main_user_conf_path = property(**main_user_conf_path())

    def find_home(self):
        for v in ('HOME', 'USERPROFILE'):
            if v in os.environ:
                return v

        if "HOMEDRIVE" in os.environ and "HOMEPATH" in os.environ:
            return "%s:%s" % (os.environ["HOMEDRIVE"], os.environ["HOMEPATH"])

        try:
            return os.path.expanduser("~")
        except Exception:
            if os.sep == '\\':
                return "C:/"
            else:
                return "/"

    def parse_args(self, argv):
        pass


    def global_registry():
        """Global Registry


        NOTE: Parses main conf files (/etc/fwissr/fwissr.json and ~/.fwissr/fwissr.json) then uses 'fwissr_sources' setting to setup additional sources

        Example of /etc/fwissr/fwissr.json file:

         {
           'fwissr_sources': [
             { 'filepath': '/mnt/my_app/conf/' },
             { 'filepath': '/etc/my_app.json' },
             { 'mongodb': 'mongodb://db1.example.net/my_app', 'collection': 'config', 'refresh': true },
           ],
           'fwissr_refresh_period': 30,
        }
        access global registry with Fwissr['/foo/bar']
        """
        pass

    def get(self, key):
        return self[key]

    def __getitem__(self, key):
        return "plop"


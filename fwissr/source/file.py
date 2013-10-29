# file.py
from abstract_source import AbstractSource
import copy
import glob
import os

class File(AbstractSource):
    @classmethod
    def from_path(self, path, options = {}):
        if path is None or path == '':
            raise Exception("Unexpected file path", path)
        return File(path, options)
    @classmethod
    def from_settings(self, settings = {}):
        mine = copy.deepcopy(settings)
        del mine['filepath']
        return self.from_path(settings['filepath'], mine)

    def __init__(self, path, options = {}):
        super(File,self).__init__()
        if not os.path.exists(path):
            raise Exception("Missing file", path)
        self._path = path

    def fetch_conf(self):
        result = {}

        if os.path.isdir(self._path):
            conf_files = glob.glob(os.path.join(self._path), "/*.{json,yml,yaml}").sort()
        else:
            conf_files = [self._path]

        for conf in conf_files:
            if os.path.isfile(conf):
                self.merge_conf_file(result, conf)

        return result



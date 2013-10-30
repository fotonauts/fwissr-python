from threading import RLock, Thread

import fwissr
import UserDict

class ReadOnlyDict(UserDict.IterableUserDict):
    def __setitem__(self, key, item): raise TypeError
    def __delitem__(self, key): raise TypeError
    def clear(self): raise TypeError
    def pop(self, key, *args): raise TypeError
    def popitem(self): raise TypeError

    def update(self, dict=None):
        if dict is None:
            pass
        elif isinstance(dict, UserDict.UserDict):
            self.data = dict.data
        elif isinstance(dict, type({})):
            self.data = dict
        else:
            raise TypeError

class ReloadThread(Thread):
    def __init__(registry):
        Thread.__init__()
        self.registry = registry
    def run():
        sleep(self.registry.refresh_period)
        self.registry.load


class Registry:
    DEFAULT_REFRESH_PERIOD = 30

    def __init__(self, refresh_period = DEFAULT_REFRESH_PERIOD):
        self._refresh_period = refresh_period

        self._registry  = {}
        self.sources = []

        self.semaphore = RLock()
        self.refresh_thread = None

    def refresh_period():
            doc = "The refresh_period property."
            def fget(self):
                    return self._refresh_period
            return locals()
    refresh_period = property(**refresh_period())

    def add_source(self, source):
        with self.semaphore:
            self.sources.append(source)
            fwissr.merge_conf(self._registry, source.get_conf())

        self.ensure_refresh_thread

    def reload(self):
        self.reset()
        self.load()

    def get(self, key):
        key_ary = key.split("/")

        if key_ary[0] == "":
            key_ary.pop(0)

        cur_hash = self._registry
        for key_component in key_ary:
            if key_component in cur_hash:
                cur_hash = cur_hash[key_component]
            else:
                return None

        return cur_hash

    def __getitem__(self,key):
        return self.get(key)


    def keys(self):
        result = []
        self._keys(result, [], self._registry)
        result.sort

    def dump(self):
        self._registry

    def refres_thread(self):
        pass

    def have_refreshable_source(self):
        with self.semaphore:
            return True in [source.can_refresh() for source in self.sources]
            return False

    def ensure_refresh_thread(self):
        if(self.refresh_period > 0) and self.have_refreshable_source() \
            and (self.refresh_thread is not None and not self.refresh_thread.is_alive()):
            # re-start refresh thread
            self.refresh_thread = ReloadThread(self)

    def reset(self):
        with self.semaphore:
            self._registry = {}
            for source in self.sources:
                source_conf = source.get_conf()
                merge_conf(self._registry, source_conf)

    def registry():
        doc = "The registry property."
        def fget(self):
            self.ensure_refresh_thread
            return self._registry
        return locals()
    registry = property(**registry())

    def _keys(self, result, key_ary, dict):
        for (key, value) in dict.items():
            key_ary.add(key)
            result = result + "/%s" % (key_ary.join("/"))
            if isinstance(value, dict):
                self._keys(result, key_ary, value) 
            key_ary.pop()




from threading import RLock, Thread

from conf import parse_conf_file, merge_conf
import UserDict
import time
import atexit

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
    def __init__(self, registry):
        super(ReloadThread, self).__init__()
        self._registry = registry
#        print "My registry is %s (and I am %s " % (registry, self)
    def run(self):
#        print "My Registry is %s" % self._registry
        count = 0
        while True:
            time.sleep(1)
#            print "%s waking up (%d/%d)" % (self, count, self._registry.refresh_period)
            if count == self._registry.refresh_period:
                self._registry.load()
#                print "%s: reloaded %s" % ( self, self._registry)
#                print "%s %s" % (self, self._registry.dump())
                count = 0
            count += 1


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
            merge_conf(self._registry, source.get_conf())

        self.ensure_refresh_thread()

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
        return sorted(result)

    def dump(self):
        return self._registry

    def refres_thread(self):
        pass

    def have_refreshable_source(self):
        with self.semaphore:
            return True in [source.can_refresh() for source in self.sources]
            return False

    def ensure_refresh_thread(self):
        if(self.refresh_period > 0) and self.have_refreshable_source() \
            and (self.refresh_thread is None or not self.refresh_thread.is_alive()):
            # re-start refresh thread
            self.refresh_thread = ReloadThread(self)
            self.refresh_thread.daemon = True
            self.refresh_thread.start()

    def reset(self):
        with self.semaphore:
            self._registry = {}
            [source.reset() for source in self.sources]

    def load(self):
        with self.semaphore:
            self._registry = {}
            for source in self.sources:
                source_conf = source.get_conf()
                merge_conf(self._registry, source_conf)
        # print "Reloaded with content: %s" % self

    def registry():
        doc = "The registry property."
        def fget(self):
            self.ensure_refresh_thread
            return self._registry
        return locals()
    registry = property(**registry())

    def _keys(self, result, key_ary, dct):
        for (key, value) in dct.items():
            key_ary.append(key)
            result.append("/%s" % ("/".join(key_ary)))
            if isinstance(value, dict):
                self._keys(result, key_ary, value)
            key_ary.pop()




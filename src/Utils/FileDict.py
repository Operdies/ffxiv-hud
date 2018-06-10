import os
import pickle
from threading import Lock, Thread
from time import sleep


def run_in_thread(fn):
    def run(*k, **kw):
        t = Thread(target=fn, args=k, kwargs=kw)
        t.start()
        return t  # <-- this is new!

    return run


class FileDict:
    def __init__(self, name, default=None):
        self.changed = False
        self.default = default
        name += '.fd'
        self.name = name
        self.saving = False

        if os.path.exists(name):
            with open(name, 'rb') as h:
                self.dict = pickle.load(h)
        else:
            self.dict = {}

    @run_in_thread
    def save_dict(self):
        """
        Writes the dictionary to disk.
        It saves after 0.5 seconds to write consecutive changes in batch
        :return:
        """
        sleep(1)
        # print('saving changes to', self.name)
        with open(self.name, 'wb') as h:
            pickle.dump(self.dict, h, pickle.HIGHEST_PROTOCOL)
        self.saving = False

    def __getitem__(self, item):
        if item in self.dict:
            return self.dict[item]
        return self.default

    def __setitem__(self, key, value):
        self.dict[key] = value
        if not self.saving:
            self.saving = True
            self.save_dict()

    def __repr__(self):
        return repr(self.dict)

    def __len__(self):
        return len(self.dict)

    def __delitem__(self, key):
        del self.dict[key]

    def clear(self):
        return self.dict.clear()

    def copy(self):
        return self.dict.copy()

    def has_key(self, k):
        return k in self.dict

    def keys(self):
        return self.dict.keys()

    def values(self):
        return self.dict.values()

    def items(self):
        return self.dict.items()

    def __contains__(self, item):
        return item in self.dict

    def __iter__(self):
        return iter(self.dict)

import ConfigParser
import logging
from storage import *
from gpg import *


class Config(object):
    def __init__(self, filename):
        self._filename = filename
        self._conf = ConfigParser.ConfigParser()
        self._conf.read(filename)
        self._storage = Storage()

    def _merge(self, a, b, path=None):
        # merges b into a
        if path is None: path = []
        for key in b:
            if key in a:
                if isinstance(a[key], dict) and isinstance(b[key], dict):
                    self._merge(a[key], b[key], path + [str(key)])
                elif a[key] == b[key]:
                    pass
                else:
                    a[key] = b[key]
            else:
                a[key] = b[key]
        return a

    def load(self, default_config = {}):
        configured = {}
        for name_section in self._conf.sections():
            configured[name_section] = dict(self._conf.items(name_section))
        merged_config = self._merge(default_config, configured)
        self._gpg = Gpg(configuration = merged_config)
        keys = self._storage.get_keys()
        if keys == []:
            print 'No gpg key registered'
            self._register_new_keys()
        else:
            if len(keys) != 2:
                print 'Problem with number of registered keys'
                exit(-1)
            keys_type = (keys[0].type, keys[1].type)
            if 'pub' and 'sec' in keys_type:
                print "ok"
            else:
                print 'Problem with key pair'
                exit(-1)
        return merged_config

    def _register_new_keys(self):
        pass

#    gpg = Gpg(configuration = merged_config)
#    gpg.srv_pub_key_exist()
#    gpg.gen_key()
#    gpg.list_keys()

import ConfigParser
import logging
from gpg import *


class Config(object):
    def __init__(self, filename):
        self._filename = filename
        self._conf = ConfigParser.ConfigParser()
        self._conf.read(filename)

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
        return merged_config

#    gpg.srv_pub_key_exist()
#    gpg.gen_keys()
#    gpg.list_keys()

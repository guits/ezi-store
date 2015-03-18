import ConfigParser
import logging
from gpg import *

class InvalidMode(Exception):
    def __init__(self, value):
        self._value = value

    def __str__(self):
        return repr(self._value)

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
        try:
            if merged_config['global']['mode'] == 'client':
                print merged_config['gpg']['server_public_key']
                print merged_config['gpg']['client_secret_key']
                print merged_config['gpg']['client_public_key']
            if merged_config['global']['mode'] == 'server':
                print merged_config['gpg']['client_public_key']
                print merged_config['gpg']['server_secret_key']
                print merged_config['gpg']['server_public_key']
            raise InvalidMode(merged_config['global']['mode'])
        except InvalidMode as err:
            print 'You must choose either client or server mode. (Configured mode: %s)' % err
            exit(-1)
        except KeyError as err:
            print "Missing parameter in configuration: %s" % err
            exit(-1)
        return merged_config

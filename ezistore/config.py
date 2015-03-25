import ConfigParser
import logging
from ezistore.gpg import *
from ezistore.tools import merge

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

    def load(self, default_config = {}):
        configured = {}
        for name_section in self._conf.sections():
            configured[name_section] = dict(self._conf.items(name_section))
        merged_config = merge(default_config, configured)
        try:
            if (merged_config['global']['mode'] != 'client') and (merged_config['global']['mode'] != 'server'):
                raise InvalidMode(merged_config['global']['mode'])
        except InvalidMode as err:
            print 'You must choose either client or server mode. (Configured mode: %s)' % err
            exit(-1)
        except KeyError as err:
            print "Missing parameter in configuration: %s" % err
            exit(-1)
        return merged_config

#    def validate(self, merged_config = {}):
#            if merged_config['global']['mode'] == 'client':
#                if (('server_public_key' not in merged_config['gpg'].keys()) or
#                   ('client_secret_key' not in merged_config['gpg'].keys()) or
#                   ('client_public_key' not in merged_config['gpg'].keys())):
#                    raise KeyError('See needed gpg parameters for client mode')
#                print merged_config['gpg']['server_public_key']
#                print merged_config['gpg']['client_secret_key']
#                print merged_config['gpg']['client_public_key']
#            elif merged_config['global']['mode'] == 'server':
#                if (('server_public_key' not in merged_config['gpg'].keys()) or
#                   ('server_secret_key' not in merged_config['gpg'].keys()) or
#                   ('client_public_key' not in merged_config['gpg'].keys())):
#                    raise KeyError('See needed gpg parameters for server mode')
#                print merged_config['gpg']['client_public_key']
#                print merged_config['gpg']['server_secret_key']
#                print merged_config['gpg']['server_public_key']

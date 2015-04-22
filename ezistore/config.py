import ConfigParser
import logging
from ezistore.tools import merge, InvalidMode

ROOT_LOG = 'ezi-store'

class Config(object):
    def __init__(self, filename):
        self._LOG = logging.getLogger("%s.%s" % (ROOT_LOG, self.__class__.__name__)) 
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
                self._LOG.error("Invalide mode in configuration : %s" % merged_config['global']['mode'])
                return None
            if (('server_key' not in merged_config['gpg'].keys()) or
               ('client_key' not in merged_config['gpg'].keys())):
                self._LOG.error("error with gpg configuration")
                return None
        except KeyError as err:
            self._LOG.error("Missing parameter in configuration: %s" % err)
            return None
        print merged_config
        return merged_config

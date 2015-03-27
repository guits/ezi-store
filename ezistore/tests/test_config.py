import unittest2 as unittest
import mock
from ezistore.config import *

class TestConfig(unittest.TestCase):

    @mock.patch('ezistore.config.ConfigParser.ConfigParser')
    def test_init(self, mock_configparser):
        filename = '/foo/bar'
        config = Config(filename)

        config._conf.sections.return_value = ['global', 'server', 'gpg', 'misc']
        #print mock_configparser._conf.sections.return_value

        config._conf.items('global').return_value = [('mode', 'server')]
        config._conf.items('server').return_value = [('bind_address', '0.0.0.0'), ('bind_port', '40000')]

        #print mock_configparser._conf.items('global').return_value
        print config._conf.items('server')

        default_config = {'global': { 'mode': 'client'}}
        merged_config = config.load(default_config = default_config)
        print merged_config

if __name__ == '__main__':
    unittest.main()

# class Config(object):
#     def __init__(self, filename):
#         self._filename = filename
#         self._conf = ConfigParser.ConfigParser()
#         self._conf.read(filename)
# 
#     def load(self, default_config = {}):
#         configured = {}
#         for name_section in self._conf.sections():
#             configured[name_section] = dict(self._conf.items(name_section))
#         merged_config = merge(default_config, configured)
#         try:
#             if (merged_config['global']['mode'] != 'client') and (merged_config['global']['mode'] != 'server'):
#                 raise InvalidMode(merged_config['global']['mode'])
#         except InvalidMode as err:
#             print 'You must choose either client or server mode. (Configured mode: %s)' % err
#             return None
#         except KeyError as err:
#             print "Missing parameter in configuration: %s" % err
#             return None
#         return merged_config

#@mockpatch('os.path')
#def foo(bar, mock):
#	pass
#
#
#def mockpatch(func):
#	def wrapper(name)
#	    mock = mockmagic()
#	    name = mock
#	    func(arg, mock)

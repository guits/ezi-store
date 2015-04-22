import unittest2 as unittest
import mock
from ezistore.config import *

class TestConfig(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestConfig, self).__init__(*args, **kwargs)
        self.filename = '/foo/bar'
        self.default_config = {'server': {
                                      'bind_address': '127.0.0.1',
                                      'bind_port': '40000'},
                          'logging': {
                                      'logfilename': '/var/log/ezistore'},
                          'gpg': {
                                  'gnupghome': '/opt/ezi-store/gpg',
                                  'key_type': 'RSA',
                                  'key_length': '4096',
                                  'expire_date': '365d',
                                  'name_real': 'Ezi Store',
                                  'name_email': 'ezi-store@zigzag.sx',
                                  'name_comment': 'ezi-store server key'}
                         }

    @mock.patch('ezistore.config.ConfigParser.ConfigParser')
    def setUp(self, mock_configparser):
        self.config = Config(self.filename)


    def test_constructor(self):
        self.config._conf.read.assert_called_once_with(self.filename)


    @mock.patch('ezistore.config.ConfigParser.ConfigParser')
    def test_load_direct_ok(self, mock_configparser):

        self.config._conf.sections.return_value = ['global', 'server', 'gpg', 'misc']
        vals = {('global',): [('mode', 'server')], ('server',): [('bind_address', '0.0.0.0'), ('bind_port', '40000')], ('gpg',): [('client_key', '1234'),('server_key', '4567')], ('misc',): [('foo', 'bar')]}
        def side_effect(*args):
            return vals[args]
        self.config._conf.items = mock.MagicMock(side_effect=side_effect)
        merged_config = self.config.load(default_config = self.default_config)

        self.assertEquals(merged_config, {'global': {'mode': 'server'}, 'misc': {'foo': 'bar'}, 'gpg': {'gnupghome': '/opt/ezi-store/gpg', 'name_real': 'Ezi Store', 'name_comment': 'ezi-store server key', 'name_email': 'ezi-store@zigzag.sx', 'key_type': 'RSA', 'expire_date': '365d', 'client_key': '1234', 'server_key': '4567', 'key_length': '4096'}, 'logging': {'logfilename': '/var/log/ezistore'}, 'server': {'bind_port': '40000', 'bind_address': '0.0.0.0'}})

    @mock.patch('ezistore.config.ConfigParser.ConfigParser')
    def test_load_invalid_mode(self, mock_configparser):

        self.config._conf.sections.return_value = ['global', 'server', 'gpg', 'misc']
        vals = {('global',): [('mode', 'other')], ('server',): [('bind_address', '0.0.0.0'), ('bind_port', '40000')], ('gpg',): [('foo', 'bar')], ('misc',): [('foo', 'bar')]}
        def side_effect(*args):
            return vals[args]
        self.config._conf.items = mock.MagicMock(side_effect=side_effect)

        merged_config = self.config.load(default_config = self.default_config)
        self.assertEquals(merged_config, None)

    @mock.patch('ezistore.config.ConfigParser.ConfigParser')
    def test_load_keyerror(self, mock_configparser):

        self.config._conf.sections.return_value = ['global', 'server', 'gpg', 'misc']
        vals = {('global',): [('foo', 'other')], ('server',): [('bind_address', '0.0.0.0'), ('bind_port', '40000')], ('gpg',): [('foo', 'bar')], ('misc',): [('foo', 'bar')]}
        def side_effect(*args):
            return vals[args]
        self.config._conf.items = mock.MagicMock(side_effect=side_effect)

        merged_config = self.config.load(default_config = self.default_config)
        self.assertEquals(merged_config, None)

    @mock.patch('ezistore.config.ConfigParser.ConfigParser')
    def test_load_missing_keys(self, mock_configparser):

        self.config._conf.sections.return_value = ['global', 'server', 'gpg', 'misc']
        vals = {('global',): [('mode', 'client')], ('server',): [('bind_address', '0.0.0.0'), ('bind_port', '40000')], ('gpg',): [('foo', 'bar')], ('misc',): [('foo', 'bar')]}
        def side_effect(*args):
            return vals[args]
        self.config._conf.items = mock.MagicMock(side_effect=side_effect)

        merged_config = self.config.load(default_config = self.default_config)
        self.assertEquals(merged_config, None)


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

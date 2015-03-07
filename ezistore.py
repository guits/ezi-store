#!/usr/bin/python

import string, sys
import ConfigParser
import re
import subprocess
import logging
import datetime
import socket
import gnupg
import storage

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ROOT_LOG = 'ezi-store'
LOG_filename = '/var/log/ezi-store'

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
        self.merged_config = self._merge(default_config, configured)
        return self.merged_config

class Gpg(object):
    def __init__(self, configure={}):
        self._LOG = logging.getLogger("%s.%s" % (ROOT_LOG, self.__class__.__name__))
        self._gpg_config = dict(configure['gpg'])
        self._gpg_gpghome = self._gpg_config['gnupghome']
        self._gpg_key_type = self._gpg_config['key_type']
        self._gpg_key_length = self._gpg_config['key_length']
        self._gpg_expire_data = self._gpg_config['expire_date']
#        self._gpg_name_real = self._gpg_config['name_real']
        self._gpg_name_real = 'ezi_store_srv'
        self._gpg_name_comment = self._gpg_config['name_comment']
        self._gpg_name_email = self._gpg_config['name_email']

        self._gpg = gnupg.GPG(gnupghome=self._gpg_config['gnupghome'])
        self._input_data = self._gpg.gen_key_input(key_type=self._gpg_key_type, key_length=self._gpg_key_length, expire_date=self._gpg_expire_data, name_real=self._gpg_name_real, name_comment=self._gpg_name_comment, name_email=self._gpg_name_email)

    def gen_key(self):
        self._gpg.gen_key(self._input_data)

    def srv_pub_key_exist(self):
        keys = self._gpg.list_keys()
        if keys == []:
            self._LOG.info('Server public key doesn\'t exist')
            return None
        print keys
#        ret = True
#        if self._gpg.list_keys() == []:
#            self._LOG.info('Public key doesn\'t exist')
#            ret = False
#        if self._gpg.list_keys(True) == []:
#            self._LOG.info('Private key doesn\'t exist')
#            ret = False
#        return retr

#    def export_armored_srv_pub_key(self, keyid):
#        return self._gpg.export_keys(keyid)
#
#    def export_armored_srv_sec_key(self, keyid):
#        return self._gpg.export_keys(keyid, True)

class Core(object):
    def __init__(self, configuration):
        self._server = Server(configuration)

    def run(self):
        for i in self._server.getmessage():
            print i

class Server(object):
    def __init__(self, configuration = {}):
        self._LOG = logging.getLogger("%s.%s" % (ROOT_LOG, self.__class__.__name__))
	self._server_bind = (configuration['default']['bind_address'], int(configuration['default']['bind_port']))
	self._LOG.info('bind to %s' % (configuration['default']['bind_address']))
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.bind(self._server_bind)
        self._sock.listen(1)

    def getmessage(self):
        while True:
            self._LOG.info('waiting for a connection')
            connection, client_address = self._sock.accept()
            print connection
            print client_address
            try:
                self._LOG.info('connection from %s %s' % (client_address[0], client_address[1]))
                while True:
                    data = connection.recv(16)
                    if data:
                        self._LOG.debug('data= %s' % (data.rstrip()))
                        yield data.rstrip()
                    else:
                        self._LOG.info('Connection closed from %s %s' % (client_address[0], client_address[1]))
                        break
            finally:
                connection.close()


def init_log():
    LOG = logging.getLogger(ROOT_LOG)
    LOG.setLevel(logging.DEBUG)

    handler_file = logging.FileHandler(filename=LOG_filename)
    handler_file.setLevel(logging.DEBUG)

    handler_stream = logging.StreamHandler()
    handler_stream.setLevel(logging.INFO)

    formatter_file = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler_file.setFormatter(formatter_file)

    formatter_stream = logging.Formatter('%(message)s')
    handler_stream.setFormatter(formatter_stream)

    LOG.addHandler(handler_file)
    LOG.addHandler(handler_stream)

if __name__ == '__main__':
    init_log()

    default_config = {'default': {'bind_address': '127.0.0.1',
                                  'bind_port': '40000'},
                      'gpg': {'gnupghome': '/opt/ezi-store/gpg',
                              'key_type': 'RSA',
                              'key_length': '4096',
                              'expire_date': '365d',
                              'name_real': 'Ezi Store',
                              'name_email': 'ezi-store@zigzag.sx',
                              'name_comment': 'ezi-store server key'}
                     }
    config = Config('/opt/ezi-store/config')
    gpg = Gpg(config.load(default_config))
    gpg.srv_pub_key_exist()
#    gpg.gen_key()
#    gpg.list_keys()
#    gpg.export_armored_srv_pub_key('CA9338C386BE60FC')
    exit(1)
    core = Core(configuration = config.load(default_config))
    core.run()

#!/usr/bin/python

import string, sys
import ConfigParser
import re
import subprocess
import logging
import datetime
import socket

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
                    print "debug"
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

class Core(object):
    def __init__(self, configuration):
        self._server = Server(config)

    def run(self):
        for i in self._server.getmessage():
            print i

class Server(object):
    def __init__(self, config = {}):
        self._LOG = logging.getLogger("%s.%s" % (ROOT_LOG, self.__class__.__name__))
        self._server_bind = (config['default']['bind-address'], int(config['default']['bind-port']))
        self._LOG.info('bind to %s' % (config['default']['bind-address']))
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

    default_config = {'default': [('bind-address', '0.0.0.0'), ('bind-port', '40000')], 'gpg': [('private-key', '/opt/ezi-store/gpg/ezi-store.key'), ('public-key', '/opt/ezi-store/gpg/ezi-store.pub')]} 
    config = Config('/opt/ezi-store/config')
    core = Core(configuration = config.load())
    core.run()

#!/usr/bin/python

import string, sys
import re
import subprocess
import logging
import datetime
import socket
import argparse
from storage import *
from config import *
from gpg import *

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ROOT_LOG = 'ezi-store'


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


def init_log(filename='/var/log/ezistore'):
    LOG = logging.getLogger(ROOT_LOG)
    LOG.setLevel(logging.DEBUG)

    handler_file = logging.FileHandler(filename=filename)
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
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", help="config file",
                        required=True, action="store", metavar="FILE")
    args = parser.parse_args()
    if args.config:
       configfilename=args.config
    else:
       configfilename='/opt/ezi-store/config'

    default_config = {'default': {'bind_address': '127.0.0.1',
                                  'bind_port': '40000',
                                  'logfilename': '/var/log/ezistore'},
                      'gpg': {'gnupghome': '/opt/ezi-store/gpg',
                              'key_type': 'RSA',
                              'key_length': '4096',
                              'expire_date': '365d',
                              'name_real': 'Ezi Store',
                              'name_email': 'ezi-store@zigzag.sx',
                              'name_comment': 'ezi-store server key'}
                     }

    config = Config(configfilename)
    merged_config = config.load(default_config)
    
    init_log(filename=merged_config['default']['logfilename'])
    gpg = Gpg(merged_config)
    gpg.srv_pub_key_exist()
#    gpg.gen_key()
#    gpg.list_keys()
#    gpg.export_armored_srv_pub_key('CA9338C386BE60FC')
    exit(1)
    core = Core(configuration = config.load(default_config))
    core.run()

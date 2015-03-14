#!/usr/bin/python

import string, sys
import re
import subprocess
import logging
import datetime
import argparse
from storage import *
from config import *
from gpg import *
from server import *

ROOT_LOG = 'ezi-store'

class Core(object):
    def __init__(self, configuration):
        self._server = Server(configuration)

    def run(self):
        for i in self._server.getmessage():
            print i

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
    
#    gpg = Gpg(configuration = merged_config)
#    gpg.srv_pub_key_exist()
#    gpg.gen_key()
#    gpg.list_keys()
#    gpg.export_armored_srv_pub_key('CA9338C386BE60FC')
    exit(1)
    core = Core(configuration = merged_config)
    core.run()

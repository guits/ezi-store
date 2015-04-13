#!/usr/bin/python

import string, sys
import re
import subprocess
import logging
import datetime
import argparse
from ezistore.storage import *
from ezistore.config import *
from ezistore.core import *

ROOT_LOG = 'ezi-store'

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

def ezistored():
    LOG = logging.getLogger("%s.%s" % (ROOT_LOG, self.__class__.__name__))
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", help="config file",
                        required=True, action="store", metavar="FILE")
    args = parser.parse_args()
    if args.config:
       configfilename=args.config
    else:
       configfilename='/opt/ezi-store/config'

    default_config = {'server': {
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
    config = Config(configfilename)
    if config == None:
        LOG.error("Can't load config file")
        return None
    merged_config = config.load(default_config)
    if merged_config == None:
        LOG.error("Can't merge config file")
        return None
    init_log(filename=merged_config['logging']['logfilename'])
    
    core = Core(configuration = merged_config)
    core.run()

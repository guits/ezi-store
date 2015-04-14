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
from ezistore.tools import *

def ezistored():
    LOG = logging.getLogger("%s" % (__name__))
    parser = argparse.ArgumentParser()
    default_config_file = '/opt/ezi-store/config'

    parser.add_argument("-c", "--config", help="specify config file, default: %s" % (default_config_file),
                         action="store", metavar="FILE", default=default_config_file)
    
    args = parser.parse_args()

    configfilename=args.config

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
    init_log(ROOT_LOG=__name__.split('.')[0], filename=merged_config['logging']['logfilename'])
    
    core = Core(configuration = merged_config)
    core.run()

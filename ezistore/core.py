#!/usr/bin/python

import string, sys
import re
import subprocess
import logging
import datetime
import argparse
from ezistore.storage import *
from ezistore.config import *
from ezistore.gpg import *
from ezistore.server import *


class Core(object):
    def __init__(self, configuration):
        self._server = Server(configuration)

    def run(self):
        for i in self._server.getmessage():
            print i


def ezistored():
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
        #TODO: Make something better
        print "Can't merge configuration"
        return None
    merged_config = config.load(default_config)
    init_log(filename=merged_config['logging']['logfilename'])
    
#    gpg = Gpg(configuration = merged_config)
#    gpg.srv_pub_key_exist()
#    gpg.gen_keys()
#    gpg.list_keys()
#    gpg.export_armored_srv_pub_key('CA9338C386BE60FC')
    exit(1)
    core = Core(configuration = merged_config)
    core.run()

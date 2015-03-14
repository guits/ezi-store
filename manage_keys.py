#!/usr/bin/python

import gnupg
import argparse
from config import *

if __name__ == '__main__':
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
    default_config_file = '/opt/ezi-store/config'

    parser = argparse.ArgumentParser()

    parser.add_argument("-c", "--config", help="specify config file, default: %s" % (default_config_file),
                         action="store", metavar="FILE")
    parser.add_argument("-g", "--generate", help="generate keys",
                         action="store_true")
    parser.add_argument("-l", "--list", help="list keys", action="store", default='all', nargs='?')
    args = parser.parse_args()
    if args.config:
       configfilename=args.config
    else:
       configfilename=default_config_file

    config = Config(configfilename)
    merged_config = config.load(default_config = default_config)
    gpg = Gpg(configuration = merged_config)

    if args.list is None:
        gpg.list_keys()
        #gpg.get_pub_keys()
       # gpg.get_sec_keys()
    if args.list == 'pub':
        gpg.get_pub_keys()
    if args.list == 'sec':
        gpg.get_sec_keys()

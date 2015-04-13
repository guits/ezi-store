#!/usr/bin/python

import gnupg
import argparse
import sys
from ezistore.config import *
from ezistore.gpg import *

def _init_args():
    default_config_file = '/opt/ezi-store/config'

    parser = argparse.ArgumentParser()

    parser.add_argument("-c", "--config", help="specify config file, default: %s" % (default_config_file),
                         action="store", metavar="FILE", default=default_config_file)
    parser.add_argument("-g", "--generate", help="generate keys",
                         action="store_true")
    parser.add_argument("-l", "--list", help="list keys", action="store_true")
    parser.add_argument("-r", "--remove", help="remove keys", action="store", nargs=1, metavar="fingerprint")
    parser.add_argument("-e", "--export-public-key", help="export a public key with armor", action="store", nargs=1, metavar="fingerprint")
    parser.add_argument("-E", "--export-secret-key", help="export key", action="store", nargs=1, metavar="fingerprint")
    parser.add_argument("-i", "--import-public-key", help="import a public key from file", action="store", metavar="FILE")
    parser.add_argument("-I", "--import-secret-key", help="import a secret key from file", action="store", metavar="FILE")


    args = parser.parse_args()

    return args

def _check_args(args=None):
    default_config = {'server': {'bind_address': '127.0.0.1',
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
    if args.config:
       configfilename=args.config

    config = Config(configfilename)
    if config == None:
        print "Can't load config file"
        return None

    merged_config = config.load(default_config = default_config)
    if merged_config == None:
        print "Can't merge configuration"
        return None
    gpg = Gpg(configuration = merged_config)

    if args.list:
        gpg.list_keys()
    if args.generate:
        gpg.gen_keys()

    if args.remove:
        gpg.remove_keys(fingerprint = args.remove)

    if args.export_secret_key:
        print gpg.export_armored_sec_key(args.export_secret_key).rstrip()
    if args.export_public_key:
        print gpg.export_armored_pub_key(args.export_public_key).rstrip()

    if args.import_public_key:
        with open(args.import_public_key, 'r') as f:
            key = f.read().rstrip()
        gpg.import_keys(key)

if __name__ == '__main__':
    args = _init_args()
    _check_args(args=args)

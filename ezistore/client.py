import logging
import socket

ROOT_LOG = 'ezi-store-cli'

class Client(object):
    def __init__(self, configuration = {}):
        self._LOG = logging.getLogger("%s.%s" % (ROOT_LOG, self.__class__.__name__))
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print configuration

import logging
import socket

class Client(object):
    def __init__(self, configuration = {}):
        self._LOG = logging.getLogger("%s" % (__name__))
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._connect(host=configuration['client']['server_address'], port=configuration['client']['server_port'])
        for i in self._sock.getmessage():
            print i

    def _connect(self, host, port):
        self._sock.connect((host, port))

    def sendmessage(self, message):
        self._sock.send(message)

    def getmessage(self):
#        data = self._socket.recv(16)
        while True:
            data = self._sock.recv(16)
            if data:
                self._LOG.debug('data= %s' % (data.rstrip()))
                yield data.rstrip()
            else:

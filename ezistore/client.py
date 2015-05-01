import logging
import socket

class Client(object):
    def __init__(self, configuration = {}):
        self._LOG = logging.getLogger("%s.%s" % (__name__,self.__class__.__name__))
        self._config = configuration

        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    def do_query(self, message=None):
        self._sock.connect((self._config['client']['server_address'], int(self._config['client']['server_port'])))
        self._sendmessage(message=message)
        return self._getmessage()

    def _connect(self, host, port):
        self._sock.connect((host, port))

    def _sendmessage(self, message):
        self._sock.send(str(message))
        self._LOG.debug('client data sent= %s', (message))

    def _getmessage(self):
        while True:
            data = self._sock.recv(2048)
            if data:
                self._LOG.debug('client data recv= %s' % (data.rstrip()))
                self.close()
                return data

    def close(self):
        self._sock.shutdown(socket.SHUT_RDWR)
        self._sock.close()

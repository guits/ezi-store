import logging
import socket

class Server(object):
    def __init__(self, configuration = {}):
        self._LOG = logging.getLogger("%s.%s" % (__name__,self.__class__.__name__))
	self._server_bind = (configuration['server']['bind_address'], int(configuration['server']['bind_port']))
	self._LOG.info('bind to %s' % (configuration['server']['bind_address']))
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._sock.bind(self._server_bind)
        self._sock.listen(1)

    def getmessage(self):
        while True:
            self._LOG.info('waiting for a connection')
            self._connection, self._client_address = self._sock.accept()
            self._LOG.info('connection from %s %s' % (self._client_address[0], self._client_address[1]))
            data = self._connection.recv(2048)
            if data:
                self._LOG.debug('srv data recv= %s' % (data.rstrip()))
                yield data.rstrip()
            else:
                self._LOG.info('Connection closed from %s %s' % (self._client_address[0], self._client_address[1]))

    def sendmessage(self, message=None):
        self._connection.sendall(message)
        self._LOG.debug('srv data sent= %s' % (message))

    def close(self):
        self._connection.shutdown(socket.SHUT_RDWR)
        self._connection.close()
        self._LOG.info('closed client connection %s:%s' % (self._client_address[0], self._client_address[1]))

    def killserver(self):
        self._sock.shutdown(socket.SHUT_RDWR)
        self._sock.close()

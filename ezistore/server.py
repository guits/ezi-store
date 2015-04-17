import logging
import socket

class Server(object):
    def __init__(self, configuration = {}):
        self._LOG = logging.getLogger("%s.%s" % (__name__,self.__class__.__name__))
	self._server_bind = (configuration['server']['bind_address'], int(configuration['server']['bind_port']))
	self._LOG.info('bind to %s' % (configuration['server']['bind_address']))
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.bind(self._server_bind)
        self._sock.listen(1)

    def getmessage(self):
        while True:
            self._LOG.info('waiting for a connection')
            self._connection, self._client_address = self._sock.accept()
            try:
                self._LOG.info('connection from %s %s' % (self._client_address[0], self._client_address[1]))
                while True:
                    data = self._connection.recv(16)
                    if data:
                        self._LOG.info('srv data recv= %s' % (data.rstrip()))
                        yield data.rstrip()
                    else:
                        self._LOG.info('Connection closed from %s %s' % (self._client_address[0], self._client_address[1]))
                        break
            finally:
                print "close here"
                self.close()

    def sendmessage(self, message=None):
        self._connection.sendall(message)
        self._LOG.info('srv data sent= %s' % (message))

    def close(self):
        self._connection.shutdown(socket.SHUT_RDWR)
        self._connection.close()

import logging
import socket

ROOT_LOG = 'ezi-store'

class Server(object):
    def __init__(self, configuration = {}):
        self._LOG = logging.getLogger("%s.%s" % (ROOT_LOG, self.__class__.__name__))
	self._server_bind = (configuration['server']['bind_address'], int(configuration['server']['bind_port']))
	self._LOG.info('bind to %s' % (configuration['server']['bind_address']))
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.bind(self._server_bind)
        self._sock.listen(1)

    def getmessage(self):
        while True:
            self._LOG.info('waiting for a connection')
            connection, client_address = self._sock.accept()
            print connection
            print client_address
            try:
                self._LOG.info('connection from %s %s' % (client_address[0], client_address[1]))
                while True:
                    data = connection.recv(16)
                    if data:
                        self._LOG.debug('data= %s' % (data.rstrip()))
                        yield data.rstrip()
                    else:
                        self._LOG.info('Connection closed from %s %s' % (client_address[0], client_address[1]))
                        break
            finally:
                connection.close()

    def sendmessage(self):
        pass

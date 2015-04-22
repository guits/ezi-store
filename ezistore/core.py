import logging
from ezistore.server import *
from ezistore.gpg import *

class Core(object):
    def __init__(self, configuration):
        self._LOG = logging.getLogger('%s.%s' % (__name__, self.__class__.__name__))
        self._config = configuration
        self._server = Server(configuration)
        self._gpg = Gpg(configuration = configuration)

    def run(self):
        try:
            for encoded_query in self._server.getmessage():
                decoded_query = self._gpg.decode(data=encoded_query, keyid=self._config['gpg']['server_key'])
                self._LOG.debug('srv decoded data recv= %s', decoded_query)
                self._server.sendmessage(message='fOObar!')
                self._server.close()
        except KeyboardInterrupt as err:
            self._server.killserver()

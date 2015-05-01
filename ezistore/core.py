import logging
from ezistore.server import *
from ezistore.gpg import *
from ezistore.storage import *

class Core(object):
    def __init__(self, configuration):
        self._LOG = logging.getLogger('%s.%s' % (__name__, self.__class__.__name__))
        self._config = configuration
        self._server = Server(configuration)
        self._gpg = Gpg(configuration = configuration)
        self._storage = Storage()

    def run(self):
        try:
            for encoded_query in self._server.getmessage():
                decoded_query = str(self._gpg.decode(data=encoded_query, keyid=self._config['gpg']['server_key']))
                self._LOG.debug('srv decoded data recv= %s', decoded_query)
                if decoded_query.split()[0] == 'FIND':
                    split_decoded_query = decoded_query.split()
                    split_decoded_query.pop(0)
                    body = ' '.join(split_decoded_query)
                    results = self._storage.get(body)
                    reply = []
                    for result in results:
                        reply.append(result.comment)
                self._server.sendmessage(message=str(self._gpg.encode(data='\n'.join(reply), keyid=self._config['gpg']['client_key'])))
                self._server.close()
        except KeyboardInterrupt as err:
            self._server.killserver()

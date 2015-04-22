from ezistore.server import *
from ezistore.gpg import *

class Core(object):
    def __init__(self, configuration):
        self._server = Server(configuration)
        self._gpg = Gpg(configuration = configuration)

    def run(self):
        try:
            for query in self._server.getmessage():
                self._server.sendmessage(message='fOObar!')
                self._server.close()
        except KeyboardInterrupt as err:
            self._server.killserver()
#        gpg.srv_pub_key_exist()
#        gpg.gen_keys()
#        gpg.list_keys()
#        gpg.export_armored_srv_pub_key('CA9338C386BE60FC')
#        exit(1)

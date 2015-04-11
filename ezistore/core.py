from ezistore.server import *

class Core(object):
    def __init__(self, configuration):
        self._server = Server(configuration)

    def run(self):
        for i in self._server.getmessage():
            print i
-

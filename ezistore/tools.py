import logging

class Colorize(object):
    _grey = '\033[1;30m'
    _red = '\033[1;31m'
    _green = '\033[1;32m'
    _yellow = '\033[1;33m'
    _blue = '\033[1;34m'
    _magenta = '\033[1;35m'
    _cyan = '\033[1;36m'
    _white = '\033[0;37m'
    _end = '\033[1;m'

    @staticmethod
    def grey(text):
        return '%s%s%s' % (Colorize._grey, text, Colorize._end)

    @staticmethod
    def red(text):
        return '%s%s%s' % (Colorize._red, text, Colorize._end)

    @staticmethod
    def green(text):
        return '%s%s%s' % (Colorize._green, text, Colorize._end)

    @staticmethod
    def yellow(text):
        return '%s%s%s' % (Colorize._yellow, text, Colorize._end)

    @staticmethod
    def blue(text):
        return '%s%s%s' % (Colorize._blue, text, Colorize._end)

    @staticmethod
    def magenta(text):
        return '%s%s%s' % (Colorize._magenta, text, Colorize._end)

    @staticmethod
    def cyan(text):
        return '%s%s%s' % (Colorize._cyan, text, Colorize._end)

    @staticmethod
    def white(text):
        return '%s%s%s' % (Colorize._white, text, Colorize._end)


class InvalidMode(Exception):
    def __init__(self, value):
        self._value = value

    def __str__(self):
        return repr(self._value)

def merge(a, b, path=None):
    # merges b into a
    if path is None: path = []
    for key in b:
        if key in a:
            if isinstance(a[key], dict) and isinstance(b[key], dict):
                merge(a[key], b[key], path + [str(key)])
            elif a[key] == b[key]:
                pass
            else:
                a[key] = b[key]
        else:
            a[key] = b[key]
    return a

def init_log(ROOT_LOG='ezi-store', filename='/var/log/ezistore'):
    LOG = logging.getLogger(ROOT_LOG)
    LOG.setLevel(logging.DEBUG)

    handler_file = logging.FileHandler(filename=filename)
    handler_file.setLevel(logging.DEBUG)

    handler_stream = logging.StreamHandler()
    handler_stream.setLevel(logging.INFO)

    formatter_file = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler_file.setFormatter(formatter_file)

    formatter_stream = logging.Formatter('%(message)s')
    handler_stream.setFormatter(formatter_stream)

    LOG.addHandler(handler_file)
    LOG.addHandler(handler_stream)

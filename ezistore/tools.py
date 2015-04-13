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

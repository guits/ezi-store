import unittest2 as unittest

from ezistore.tools import merge

class TestTools(unittest.TestCase):

    def test_merge(self):
        foo = { 'foo': 'foo' }
        bar = { 'bar': 'bar' }
        foobar = { 'foo': 'foo', 'bar': 'bar' }

        merged = merge(foo, bar)

        self.assertEqual(merged, foobar)

if __name__ == '__main__':
    unittest.main()

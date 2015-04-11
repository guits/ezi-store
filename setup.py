#!/usr/bin/env python

from setuptools import setup

setup(name='ezi-store',
      version='0.1',
      description=('This is a very simple password keeper based on sqlite storage '
                   'and asymmetric gpg encryption'),
      author='guits',
      author_email='guits@zigzag.sx',
      url='https://github.com/guits/ezi-store',
      packages=['ezistore'],
      scripts=['ezistored'],
     )

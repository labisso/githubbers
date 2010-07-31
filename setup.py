#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import sys
Version=0.1

setup(name='githubbers',
      version=Version,
      description='GitHub project contributors formatting utility',
      author='David LaBissoniere',
      author_email='labisso@gmail.com',
      url='http://www.github.com/labisso/githubbers',
      packages=['githubbers'],
       entry_points = {
        'console_scripts': [
            'githubbers = githubbers.main:main'
        ]
      },
      license="Apache2",
      install_requires = ['httplib2', 'pyYAML', 'Jinja2'],
     )

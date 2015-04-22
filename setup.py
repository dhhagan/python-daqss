'''
	Python wrapper for the DAQSS API

	Written originally by David H Hagan
	April 2015

'''
__version__ = '0.0.5'

import os

try:
	from setuptools import setup
except ImportError:
	from distutil.core import setup

setup(
	name = 'daqss',
	version = __version__,
	description = 'Python wrapper for the DAQSS API',
	keywords = ['DAQSS', 'MIT', 'Air Quality'],
	author = 'David H Hagan',
	author_email = 'david@davidhhagan.com',
	url = 'https://github.com/dhhagan/python-daqss',
	license = 'MIT',
	packages = ['daqss'],
	zip_safe = False,
	install_requires = ['requests'])
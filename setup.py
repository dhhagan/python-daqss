'''
	Python wrapper for the DAQSS API

	Written originally by David H Hagan
	April 2015

'''
__version__ = '0.1.0'

from distutils.core import setup

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
	classifiers = [
		'Development Status :: 1 - alpha',
		'Operating System :: OS Independent',
		'Intended Audience :: Science/Research',
		'Programming Language :: Python :: 3',
		'Topic :: Software Development',
		'Topic :: System :: Software',
		'Topic :: API',
		'Topic :: Software Development :: Libraries :: Python Modules'
	]
)

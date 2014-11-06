import os
import re

v = open(os.path.join(os.path.dirname(__file__), 'pyexperian', '__init__.py'))
VERSION = re.compile(r".*__version__ = '(.*?)'", re.S).match(v.read()).group(1)
v.close()

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Python wrapper for Experian\'s Net Connect API',
    'author': 'Carlos Eduardo Rivera',
    'url': 'https://github.com/AbleEng/pyexperian',
    'download_url': 'https://github.com/AbleEng/pyexperian',
    'author_email': 'carlos@hiable.com',
    'version': VERSION,
    'install_requires': ['requests>=2.2.1', 'xmltodict>=0.9.0'],
    'test_requires': ['nose>=1.3.4'],
    'packages': ['pyexperian', 'pyexperian.test', 'pyexperian.lib'],
    'scripts': [],
    'name': 'pyexperian',
    'keywords': 'experian net connect ecals'
}

setup(**config)
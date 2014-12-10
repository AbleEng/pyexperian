try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'version': '0.12.7',
    'description': 'Python wrapper for Experian\'s Net Connect API',
    'author': 'Carlos Eduardo Rivera',
    'url': 'https://github.com/AbleEng/pyexperian',
    'download_url': 'https://github.com/AbleEng/pyexperian',
    'author_email': 'carlos@hiable.com',
    'install_requires': ['requests>=2.2.1', 'xmltodict>=0.9.0'],
    'tests_require': ['nose>=1.3.4'],
    'packages': ['pyexperian', 'pyexperian.test', 'pyexperian.lib'],
    'scripts': [],
    'name': 'pyexperian',
    'keywords': 'experian netconnect ecals'
}

setup(**config)

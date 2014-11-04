try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'PyExperian',
    'author': 'Carlos Eduardo Rivera',
    'url': 'https://github.com/AbleEng/pyexperian',
    'download_url': 'https://github.com/AbleEng/pyexperian',
    'author_email': 'carlos@hiable.com',
    'version': '0.1',
    'install_requires': ['nose', 'requests', 'xmltodict'],
    'packages': ['pyexperian'],
    'scripts': [],
    'name': 'pyexperian'
}

setup(**config)
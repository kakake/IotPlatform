try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


config = {
    'description': 'IotPlatform',
    'author': 'kakake',
    'url': 'www.efwplus.cn',
    'download_url': 'www.efwplus.cn',
    'author_email': '343588387@qq.com',
    'version': '0.1',
    'install_requires': ['nose','libhttp2'],
    'packages': ['iotserver'],
    'scripts': [],
    'name': 'iotserver'
}


setup(**config)

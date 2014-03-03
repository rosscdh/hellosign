from distutils.core import setup
from setuptools import find_packages
from hellosign.version import __version__

setup(
    name='hellosign',
    packages=['hellosign'],
    version=__version__,
    author="Ross Crawford-d'Heureuse",
    author_email='sendrossemail@gmail.com',
    include_package_data=True,
    url='https://github.com/rosscdh/hellosign',
    download_url='https://github.com/rosscdh/hellosign/archive/0.1.1.tar.gz',
    description='Module for interacting with the HelloSign service',
    zip_safe=False,
    install_requires=[
        'WTForms',
        'requests',
        'nose',
        'querystring_parser',
        'mocktest'
     ]
)

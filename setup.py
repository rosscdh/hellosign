from distutils.core import setup
from setuptools import find_packages

setup(
    name='hellosign',
    version='0.1.1',
    author="Ross Crawford-d'Heureuse",
    author_email='sendrossemail@gmail.com',
    packages=['hellosign'],
    include_package_data=True,
    url='https://github.com/rosscdh/hellosign',
    download_url='https://github.com/rosscdh/hellosign/archive/0.1.1.tar.gz'
    description='Module for interacting with the HelloSign service',
    long_description=open('README.md').read(),
    zip_safe=False,
    install_requires=[
        'WTForms',
        'requests',
        'nose',
        'querystring_parser',
        'mocktest'
     ]
)

from distutils.core import setup
from setuptools import find_packages

setup(
    name='hellosign',
    version='0.1.0',
    author="Ross Crawford-d'Heureuse",
    author_email='sendrossemail@gmail.com',
    packages=['hellosign'],
    include_package_data=True,
    url='https://github.com/stard0g101/HelloSignApi',
    description='Module for interacting with the HelloSign service',
    long_description=open('README.md').read(),
    zip_safe=False,
    install_requires=[
        'WTForms',
        'requests',
        'nose',
        'querystring-parser',
        'mocktest'
     ]
)

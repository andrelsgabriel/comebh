#!/usr/bin/env python

from setuptools import setup

setup(
    name='mycms',
    version='1.0',
    description='OpenShift App',
    author='Ken Cochrane',
    author_email='example@example.com',
    url='http://www.python.org/sigs/distutils-sig/',
    install_requires=['Django>=1.3', 
                      'PIL==1.1.7', 
                      'django-cms==2.2', 
                      'south==0.7.2', 
                      'MySQL-python==1.2.3'
                      ],
)

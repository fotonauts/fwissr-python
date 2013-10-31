#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

setup(
    name='fwissr',
    version='0.1.0',
    description='fwissr is a registry configuration tool, compatible with fwissr',
    long_description=readme + '\n\n' + history,
    author='Pierre Baillet',
    author_email='pierre@baillet.name',
    url='https://github.com/fotonauts/fwissr-python',
    packages=[
        'fwissr',
    ],
    package_dir={'fwissr': 'fwissr'},
    include_package_data=True,
    install_requires=[
        'pymongo>=2.5.2',
        'PyYAML>=3.10'
    ],
    license="MIT",
    zip_safe=False,
    keywords='fwissr',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
    ],
    test_suite='tests',
)

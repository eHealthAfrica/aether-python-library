#!/usr/bin/env python

# Copyright (C) 2019 by eHealth Africa : http://www.eHealthAfrica.org
#
# See the NOTICE file distributed with this work for additional information
# regarding copyright ownership.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

import os
from io import open
from setuptools import setup, find_packages


def read(f):
    return open(f, 'r', encoding='utf-8').read()


VERSION = os.environ.get('VERSION', '0.0.0')


setup(
    version=VERSION,
    name='aether.python',
    description='A python library with Aether Python functionality',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',

    keywords=[
        'aether',
        'entity',
        'extraction',
        'redis',
        'utils',
        'validators',
    ],

    url='https://github.com/eHealthAfrica/aether-python-library/',
    author='eHealth Africa',
    author_email='aether@ehealthafrica.org',
    license='Apache2 License',

    python_requires='>=3.7',
    install_requires=[
        'eha_jsonpath',
        'jsonschema',
        'redis',
        'requests[security]',
        'spavro',
    ],
    extras_require={
        'test': [
            'birdisle',
            'coverage',
            'flake8',
            'flake8-quotes',
            'tblib',  # for paralell test runner
        ],
    },
    packages=find_packages(exclude=['*tests*']),
    include_package_data=True,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Plugins',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)

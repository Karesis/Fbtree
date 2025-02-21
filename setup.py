#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
from setuptools import setup, find_packages

# Read the package version from __init__.py
with open(os.path.join('fbtree', '__init__.py'), 'r', encoding='utf-8') as f:
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", f.read(), re.M)
    version = version_match.group(1) if version_match else '0.1.0'

# Read the README file for the long description
with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='fbtree',
    version=version,
    author='Karesis',
    author_email='yangyifeng23@mails.ucas.ac.cn',
    description='A path-oriented database for storing and analyzing sequential decision paths',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Karesis/Fbtree',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Database',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Software Development :: Libraries',
    ],
    keywords=[
        'decision-tree', 
        'database', 
        'sequential-data', 
        'path-analysis', 
        'decision-making'
    ],
    python_requires='>=3.7',
    install_requires=[
        # 列出您的项目依赖，例如：
        # 'numpy>=1.20.0',
    ],
    extras_require={
        'dev': [
            'pytest>=6.0',
            'black',
            'flake8',
            'mypy',
            'isort',
        ],
        'docs': [
            'sphinx',
            'sphinx-rtd-theme',
        ],
    },
    project_urls={
        'Documentation': 'https://github.com/Karesis/Fbtree#readme',
        'Bug Reports': 'https://github.com/Karesis/Fbtree/issues',
        'Source Code': 'https://github.com/Karesis/Fbtree',
    },
    include_package_data=True,
    zip_safe=False,
)
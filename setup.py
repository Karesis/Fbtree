#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
from setuptools import setup, find_packages

# Read the package version from __init__.py
with open(os.path.join('fbtree', '__init__.py'), 'r', encoding='utf-8') as f:
    for line in f:
        if line.startswith("__version__"):
            version = line.split("=")[1].strip().strip('"\'')
            break

# Read the README file for the long description
try:
    with open('README.md', 'r', encoding='utf-8') as f:
        long_description = f.read()
except UnicodeDecodeError:
    # 如果UTF-8解码失败，尝试使用其他编码
    try:
        with open('README.md', 'r', encoding='gbk') as f:
            long_description = f.read()
    except UnicodeDecodeError:
        # 如果还是失败，使用简单描述
        long_description = "FiberTree - 专注于存储和分析顺序决策路径的数据库系统"

setup(
    name='fbtree',
    version=version,
    author='杨亦锋 (Karesis)',
    author_email='yangyifeng23@mails.ucas.ac.cn',
    description='专注于存储和分析顺序决策路径的数据库系统',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Karesis/Fbtree',
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Database',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
    ],
    keywords=[
        'decision tree', 
        'database', 
        'analysis', 
        'decision paths', 
        'statistics'
    ],
    python_requires='>=3.6',
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
    zip_safe=False,
)
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import codecs

try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

setup(
    name='chishop',
    version=__import__('djangopypi').__version__,
    description='Simple PyPI server written in Django.',
    author='Ask Solem',
    author_email='askh@opera.com',
    packages=["djangopypi"],
    install_requires=[
        'django>=1.0',
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python",
    ],
    long_description=codecs.open('README', "r", "utf-8").read(),
)

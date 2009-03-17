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

from distutils.command.install_data import install_data
from distutils.command.install import INSTALL_SCHEMES
import sys

djangopypi = __import__('djangopypi', {}, {}, [''])

packages, data_files = [], []
root_dir = os.path.dirname(__file__)
if root_dir != '':
    os.chdir(root_dir)
djangopypi_dir = "djangopypi"

def osx_install_data(install_data):
    def finalize_options(self):
        self.set_undefined_options("install", ("install_lib", "install_dir"))
        install_data.finalize_options(self)

#if sys.platform == "darwin":
#    cmdclasses = {'install_data': osx_install_data}
#else:
#    cmdclasses = {'install_data': install_data}


def fullsplit(path, result=None):
    if result is None:
        result = []
    head, tail = os.path.split(path)
    if head == '':
        return [tail] + result
    if head == path:
        return result
    return fullsplit(head, [tail] + result)


for scheme in INSTALL_SCHEMES.values():
    scheme['data'] = scheme['purelib']


for dirpath, dirnames, filenames in os.walk(djangopypi_dir):
    # Ignore dirnames that start with '.'
    for i, dirname in enumerate(dirnames):
        if dirname.startswith("."): del dirnames[i]
    for filename in filenames:
        if filename.endswith(".py"):
            packages.append('.'.join(fullsplit(dirpath)))
        else:
            data_files.append([dirpath, [os.path.join(dirpath, f) for f in
                filenames]])
setup(
    name='chishop',
    version=djangopypi.__version__,
    description='Simple PyPI server written in Django.',
    author='Ask Solem',
    author_email='askh@opera.com',
    packages=packages,
    url="http://ask.github.com/chishop",
    zip_safe=False,
    data_files=data_files,
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
        "Topic :: System :: Software Distribution",
        "Programming Language :: Python",
    ],
    long_description=codecs.open('README', "r", "utf-8").read(),
)

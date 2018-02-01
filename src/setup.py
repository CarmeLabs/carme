#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""
from codecs import open
from os.path import abspath, dirname, join
from subprocess import call
from setuptools import Command, find_packages, setup
from carme import __version__

this_dir = abspath(dirname(__file__))

with open(join(this_dir, 'README.rst'), encoding='utf-8') as file:
    long_description = file.read()

class RunTests(Command):
    """Run all tests."""
    description = 'run tests'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        """Run all tests!"""
        errno = call(['py.test', '--cov=carme', '--cov-report=term-missing'])
        raise SystemExit(errno)


setup(
    name = 'carme',
    version = '0.0.7',
    description = 'An opinionated AI stack built for Kubernetes by default',
    long_description = long_description,
    url = 'https://github.com/carme/carme',
    author = 'Jason Kuruzovich',
    author_email = 'jkuruzovich@gmail.com',
    classifiers = [
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
        ],
    keywords='kubernetes analytics jupyterhub airflow',
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    install_requires=['ruamel.yaml','docopt'],
    include_package_data=True,
    extras_require = {
        'test': ['coverage', 'pytest', 'pytest-cov'],
    },
    entry_points={
        'console_scripts': [
            'carme=carme.cli:main'
        ],
    },
    cmdclass = {'test': RunTests},
)

#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""
from codecs import open
from os.path import abspath, dirname, join
from unittest import TestLoader
from setuptools import find_packages, setup
from src import __version__
#from subprocess import call
#from setuptools import Command, find_packages, setup
#from pip.req import parse_requirements

THIS_DIR = abspath(dirname(__file__))

with open(join(THIS_DIR, 'README.md'), encoding='utf-8') as file:
    LONG_DESCRIPTION = file.read()

'''
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
'''

def test_suite():
    """runs the test suite"""
    return TestLoader().discover('tests')

setup(
    name='carme',
    version='0.0.1',
    description='An opinionated AI stack built for Kubernetes by default',
    long_description=LONG_DESCRIPTION,
    url='https://github.com/carme/carme',
    author='Jason Kuruzovich',
    author_email='jkuruzovich@gmail.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
        ],
    keywords='kubernetes analytics jupyterhub airflow',
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    install_requires=["docker", "click", "ruamel.yaml", "validators", "gitconfig"],
    include_package_data=True,
    extras_require={
        'test': ['coverage', 'pytest', 'pytest-cov'],
    },
    entry_points={
        'console_scripts': [
            'carme=src.cli.cli:carme'
        ],
    },
    # cmdclass = {'test': RunTests},
    test_suite='tests',
)

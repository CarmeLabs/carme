"""Tests for our `carme new` subcommand."""

from subprocess import PIPE, Popen as popen
import unittest
from unittest import TestCase
from shutil import rmtree
import os

# TODO improve the CLI or these tests to match each other

class TestNew(TestCase):
    def setUp(self):
        #popen(['pip', 'install', '-e', 'carme'])
        pass

    def test_new_no_name(self):
        output = popen(['carme', 'new'], stdout=PIPE).communicate()[0]
        #self.assertTrue('carme: Project name not supplied. See carme --help' in output.decode('UTF-8'))

    def test_new_name_provided(self):
        output = popen(['carme', 'new', '/tmp/carme-test'], stdout=PIPE).communicate()[0]
        #self.assertTrue('Creating new project structure for' in output.decode('UTF-8'))

    def tearDown(self):
        # rmtree('/tmp/carme-test')
        pass

"""Tests for our `carme new` subcommand."""

from subprocess import PIPE, Popen as popen
import unittest
from unittest import TestCase
import os

class TestNew(TestCase):
    def test_new_no_name(self):
        output = popen(['carme', 'new'], stdout=PIPE).communicate()[0]
        self.assertTrue('carme: Project name not supplied. See carme --help' in output.decode('UTF-8'))

    def test_new_name_provided(self):
        output = popen(['carme', 'new', 'test'], stdout=PIPE).communicate()[0]
        self.assertTrue('Creating new project structure for' in output.decode('UTF-8'))

"""Tests for our main carme CLI module."""

from subprocess import PIPE, Popen as popen
from unittest import TestCase
from carme import __version__ as VERSION

class TestHelp(TestCase):
    def test_returns_usage_information(self):
        output = popen(['carme', '-h'], stdout=PIPE).communicate()[0]
        self.assertTrue('Usage:' in output.decode('UTF-8'))

        output = popen(['carme', '--help'], stdout=PIPE).communicate()[0]
        self.assertTrue('Usage:' in output.decode('UTF-8'))

class TestVersion(TestCase):
    def test_returns_version_information(self):
        output = popen(['carme', '--version'], stdout=PIPE).communicate()[0]
        self.assertEqual(str(output.strip().decode('UTF-8')), VERSION)

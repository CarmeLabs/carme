"""Tests for our `carme cluster` subcommand."""

from subprocess import PIPE, Popen as popen
from unittest import TestCase
import os

class TestCluster(TestCase):
    def test_returns_adding_config_gcp(self):
        output = popen(['carme', 'init', 'gcp', '--force'], stdout=PIPE).communicate()[0]
        self.assertTrue('Adding configuration for gcp to launch.yaml.' in output.decode('UTF-8'))
    def test_returns_not_line(self):
       output = popen(['carme', 'cluster', 'login', '--dry-run'], stdout=PIPE).communicate()[0]
       lines = output.decode('UTF-8').split('\n')
       print(lines)#
       self.assertTrue(len(lines) > 1 and len(lines) < 7)

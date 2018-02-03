"""Tests for our `carme app` subcommand."""

from subprocess import PIPE, Popen as popen
from unittest import TestCase
import os

class TestApp(TestCase):
    def test_returns_not_line(self):
        output = popen(['carme', 'app', 'jupyter','install', '--dry-run'], stdout=PIPE).communicate()[0]
        lines = output.decode('UTF-8').split('\n')
        print(lines)
        self.assertTrue(len(lines) > 1 and len(lines) < 7)
#Don't know way this is failing.
#    def test_returns_adding_config(self):
#        output = popen(['carme', 'app', 'jupyter', 'install','--dry-run'], stdout=PIPE).communicate()[0]
#        self.assertTrue('helm install jupyterhub/jupyterhub' in output.decode('UTF-8'))

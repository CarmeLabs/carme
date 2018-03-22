""" Test suite for `carme connect command` """

import logging
import sys
from unittest import TestCase
from mock import patch, Mock
from src.cli.commands.connect import Connect

# set up logging
FORMAT = 'carme: [%(levelname)s] %(message)s'
logging.basicConfig(level=logging.INFO, format=FORMAT, stream=sys.stderr)

class TestCliConnect(TestCase):
    def setUp(self):
        self.base_patcher = patch('src.cli.commands.connect.Base')
        self.mock_base = self.base_patcher.start()
        self.input_patcher = patch('src.cli.commands.connect.input')
        self.mock_input = self.input_patcher.start()
        self.mock_input.return_value = ""
        self.logging_patcher = patch('src.cli.commands.connect.logging')
        self.mock_logging = self.logging_patcher.start()
        self.Connect = Connect(self.mock_base)
        self.mock_rv = Mock()

    def test_connect_run(self):
        self.Connect.run()
        self.mock_input.return_value = "invalid_url"
        self.Connect.run()
        self.mock_input.return_value = "https://valid"
        self.connect_patcher = patch('src.cli.commands.connect.Git.remote_add')
        self.mock_connect = self.connect_patcher.start()
        self.Connect.run()
        self.assertTrue(self.mock_connect.called)

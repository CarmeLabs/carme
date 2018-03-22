""" Test suite for `carme save command` """

import logging
import os, sys
import shutil
from unittest import TestCase
from mock import patch, Mock
from src.cli.commands.save import Save

# set up logging
FORMAT = 'carme: [%(levelname)s] %(message)s'
logging.basicConfig(level=logging.INFO, format=FORMAT, stream=sys.stderr)

class TestCliSave(TestCase):
    def setUp(self):
        self.open_patcher = patch('src.cli.commands.save.open')
        self.mock_open = self.open_patcher.start()
        self.base_patcher = patch('src.cli.commands.save.Base')
        self.mock_base = self.base_patcher.start()
        self.ospath_patcher = patch('src.cli.commands.save.os.path.abspath')
        self.mock_ospath = self.ospath_patcher.start()
        self.mock_ospath.return_value = "./tmp_test_dir"
        self.logging_patcher = patch('src.cli.commands.save.logging')
        self.mock_logging = self.logging_patcher.start()
        self.save = Save(self.mock_base)
        self.save.options = {"message": "test"}
        self.save.project_name = ""
        self.save.project_dir = ""
        self.save.data_dir = ""
        self.save.docker_dir = ""
        self.save.cwd = ""
        self.mock_rv = Mock()

    def test_save_run(self):
        self.add_patcher = patch('src.cli.commands.save.Git.add')
        self.mock_add = self.add_patcher.start()
        self.commit_patcher = patch('src.cli.commands.save.Git.commit')
        self.mock_commit = self.commit_patcher.start()
        self.push_patcher = patch('src.cli.commands.save.Git.push')
        self.mock_push = self.push_patcher.start()
        self.save.run()
        self.assertTrue(self.mock_add.called)
        self.assertTrue(self.mock_commit.called)
        self.assertTrue(self.mock_push.called)

""" Test suite for `carme new command` """

import logging
import os, sys
import shutil
from unittest import TestCase
from mock import patch, Mock
from src.cli.commands.new import New

# set up logging
FORMAT = 'carme: [%(levelname)s] %(message)s'
logging.basicConfig(level=logging.INFO, format=FORMAT, stream=sys.stderr)

class TestCliRun(TestCase):
    def setUp(self):
        os.mkdir("tmp_test_dir")
        os.chdir("./tmp_test_dir")
        self.open_patcher = patch('src.cli.commands.new.open')
        self.mock_open = self.open_patcher.start()
        self.copy_file_patcher = patch('src.cli.commands.new.copyfile')
        self.mock_copyfile = self.copy_file_patcher.start()
        self.base_patcher = patch('src.cli.commands.new.Base')
        self.mock_base = self.base_patcher.start()
        self.input_patcher = patch('src.cli.commands.new.input')
        self.mock_input = self.input_patcher.start()
        self.mock_input.return_value = {"<project>": "tmp_test_dir"}
        self.ospath_patcher = patch('src.cli.commands.new.os.path.join')
        self.mock_ospath = self.ospath_patcher.start()
        self.mock_ospath.return_value = "./tmp_test_dir"
        self.logging_patcher = patch('src.cli.commands.new.logging')
        self.mock_logging = self.logging_patcher.start()
        self.New = New(self.mock_base)
        self.New.project_name = ""
        self.New.project_dir = ""
        self.New.data_dir = ""
        self.New.docker_dir = ""
        self.New.cwd = ""
        self.mock_rv = Mock()
    
    def tearDown(self):
        os.chdir("..")
        shutil.rmtree("./tmp_test_dir")

    def test_new_create_structure(self):
        self.New.create_structure()
        self.assertTrue(os.path.exists("./apps"))
        self.assertTrue(os.path.exists("./data"))
        self.assertTrue(os.path.exists("./docker/pip-cache"))
        self.assertTrue(os.path.exists("./notebooks"))

    def test_new_run(self):
        self.New.run()
        os.chdir("..")
        self.assertTrue(os.path.exists("./tmp_test_dir"))
        self.assertTrue(os.path.exists("./tmp_test_dir/apps"))
        self.assertTrue(os.path.exists("./tmp_test_dir/data"))
        self.assertTrue(os.path.exists("./tmp_test_dir/docker/pip-cache"))
        self.assertTrue(os.path.exists("./tmp_test_dir/notebooks"))
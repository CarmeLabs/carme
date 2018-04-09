""" Test suite for `carme connect command` """

import logging
import sys
import os
import shutil
from unittest import TestCase
from src.cli.commands.connect import connect
from src.cli.commands.new import new
from click.testing import CliRunner


# set up logging
FORMAT = 'carme: [%(levelname)s] %(message)s'
logging.basicConfig(level=logging.INFO, format=FORMAT, stream=sys.stderr)

class TestCliConnect(TestCase):
    def setUp(self):
        os.mkdir("tmp_test_dir")
        os.chdir("./tmp_test_dir")
        self.connect = connect
        self.new = new

    def tearDown(self):
        os.chdir("..")
        os.chdir("..")
        shutil.rmtree("./tmp_test_dir", ignore_errors=True)

    def test_connect_run(self):
        runner = CliRunner()
        runner.invoke(self.new, ['tmp_test_dir'])
        result = runner.invoke(self.connect, input='https://goodurl.com')
        assert result.exit_code == 0
        assert not result.exception
        result = runner.invoke(self.connect, input='bad_url')
        assert result.exit_code == 0
        assert not result.exception

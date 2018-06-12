""" Test suite for `carme save command` """

import logging
import os, sys
import shutil
from unittest import TestCase
from src.cli.commands.save import save
from src.cli.commands.new import new
from click.testing import CliRunner

# set up logging
FORMAT = 'carme: [%(levelname)s] %(message)s'
logging.basicConfig(level=logging.INFO, format=FORMAT, stream=sys.stderr)

class TestCliSave(TestCase):
    def setUp(self):
        os.mkdir("tmp_test_dir")
        os.chdir("./tmp_test_dir")
        self.new = new
        self.save = save

    def tearDown(self):
        os.chdir("../..")
        shutil.rmtree("./tmp_test_dir")

    def test_save_run(self):
        runner = CliRunner()
        runner.invoke(new, ['tmp_test_dir'])
        result = runner.invoke(save, ['--nopush'])
        assert result.exit_code == 0
        assert not result.exception

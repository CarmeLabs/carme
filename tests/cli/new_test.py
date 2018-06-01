""" Test suite for `carme new command` """

import logging
import os, sys
import shutil
from unittest import TestCase
from src.cli.commands.new import new
from click.testing import CliRunner

# set up logging
FORMAT = 'carme: [%(levelname)s] %(message)s'
logging.basicConfig(level=logging.INFO, format=FORMAT, stream=sys.stderr)

class TestCliRun(TestCase):
    def setUp(self):
        os.mkdir("tmp_test_dir")
        os.chdir("./tmp_test_dir")
        self.new = new

    def tearDown(self):
        os.chdir("..")
        shutil.rmtree("./tmp_test_dir")

    def test_new_run(self):
        runner = CliRunner()
        result = runner.invoke(self.new, ['tmp_test_dir'])
        os.chdir("..")
        self.assertTrue(os.path.exists("./tmp_test_dir"))
        self.assertTrue(os.path.exists("./tmp_test_dir/apps"))
        self.assertTrue(os.path.exists("./tmp_test_dir/data"))
        self.assertTrue(os.path.exists("./tmp_test_dir/docker"))

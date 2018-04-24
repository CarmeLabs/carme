""" Test suite for the gitwrapper module"""

import logging
import os, sys
from unittest import TestCase
from mock import patch, Mock
from src.modules.gitwrapper import Git

# set up logging
FORMAT = 'carme: [%(levelname)s] %(message)s'
logging.basicConfig(level=logging.INFO, format=FORMAT, stream=sys.stderr)

class TestGitWrapper(TestCase):
    def setUp(self):
        self.git = Git()
        self.popen_patcher = patch('src.modules.gitwrapper.Popen')
        self.mock_popen = self.popen_patcher.start()
        self.input_patcher = patch('src.modules.gitwrapper.input')
        self.mock_input = self.input_patcher.start()
        self.getpass_patcher = patch('src.modules.gitwrapper.getpass')
        self.mock_getpass = self.getpass_patcher.start()
        self.mock_rv = Mock()
        self.mock_popen.return_value = self.mock_rv

    def test_git_init(self):
        self.assertRaises(ValueError, Git.init, "")
        self.assertRaises(ValueError, Git.init, "//invalid/directory/")
        Git.init(os.getcwd())

    def test_git_add(self):
        self.assertRaises(ValueError, Git.add, "")
        self.assertRaises(ValueError, Git.add, "//invalid/directory/")
        Git.add(os.getcwd())

    def test_git_commit(self):
        self.assertRaises(ValueError, Git.commit, "", "")
        self.assertRaises(ValueError, Git.commit, "//invalid/directory/", "")
        Git.commit("", os.getcwd())

    def test_git_remote_add(self):
        self.assertRaises(ValueError, Git.remote_add, "", "")
        self.assertRaises(ValueError, Git.remote_add, "", "//invalid/directory/")
        Git.remote_add(os.getcwd(), "")

    def test_git_push(self):
        self.assertRaises(ValueError, Git.push, "")
        self.assertRaises(ValueError, Git.push, "//invalid/directory/")
        self.mock_rv.communicate.return_value = ["", ""]
        self.assertRaises(ValueError, Git.push, os.getcwd())
        self.mock_rv.communicate.return_value = ["invalid_url", ""]
        self.assertRaises(ValueError, Git.push, os.getcwd())
        self.mock_rv.communicate.return_value = ["https://validurl.com", ""]
        Git.push(os.getcwd())

    def test_git_log(self):
        self.mock_rv.communicate.return_value = [b'test', ""]
        Git.log()
        Git.log(1, [])
        Git.log(1, ['-f'])


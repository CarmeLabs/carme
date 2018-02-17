'''
Connects to the github repo
'''

from .base import Base
import os
import sys
import validators
import logging
import subprocess
from .git import Git

# Set up logger
FORMAT = 'carme: [%(levelname)s] %(message)s'
logging.basicConfig(level=logging.INFO, format=FORMAT)

class Connect(Base):
    def run(self):
        # Get this scripts dir
        self.base_dir=os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
        self.cwd=os.getcwd()
        self.git = Git()
        remote_repo = input("Enter remote git repository URL: ")
        if(validators.url(remote_repo)):
            try:
                self.git.remote_add(self.cwd, remote_repo)
                logging.info("Successfully connected project to " + remote_repo)
            except Exception as err:
                logging.error(err)
        else:
            logging.error("Invalid URL. Please see carme --help")

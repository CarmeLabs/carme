'''
Connects to the github repo
'''

from .base import Base
import os
import sys
import logging
import subprocess
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)) + "/../modules")
from gitwrapper import Git

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
        if len(remote_repo) == 0:
            logging.error("Git URL cannot be empty")
        elif remote_repo.find("https://") == -1:
            logging.error("Invalid git URL")
        else:
            try:
                self.git.remote_add(self.cwd, remote_repo)
                logging.info("Successfully connected project to " + remote_repo)
            except Exception as err:
                logging.error(err)

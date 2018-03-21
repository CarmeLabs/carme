'''
Connects to the github repo
'''

import os
import logging
from .base import Base
from ...modules.gitwrapper import Git

# Set up logger
FORMAT = 'carme: [%(levelname)s] %(message)s'
logging.basicConfig(level=logging.INFO, format=FORMAT)

class Connect(Base):
    """
    CLI command for connecting to a github repository

    Attributes:
        git (object): Wrapper for git commands
        base_dir (str): Directory to the file
        cwd (str): Current working directory of the instance

    """
    
    def run(self):
        """
        Connects the carme project to a github repository

        Throws
        -------
        Exception if error occurs when running git remote add
        """
        self.base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
        self.cwd = os.getcwd()
        self.git = Git()
        remote_repo = input("Enter remote git repository URL: ")
        if not remote_repo:
            logging.error("Git URL cannot be empty")
        elif remote_repo.find("https://") == -1:
            logging.error("Invalid git URL")
        else:
            try:
                self.git.remote_add(self.cwd, remote_repo)
                logging.info("Successfully connected project to %s", remote_repo)
            except Exception as err:
                logging.error(err)

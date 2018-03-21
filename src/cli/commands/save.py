'''
Saves the project
'''

import os
import logging
from .base import Base
from ...modules.gitwrapper import Git


# Set up logger
FORMAT = 'carme: [%(levelname)s] %(message)s'
logging.basicConfig(level=logging.INFO, format=FORMAT)

class Save(Base):
    """
    CLI command for saving to a github repository

    Attributes:
        git (object): Wrapper for git commands
        base_dir (str): Directory to the file
        cwd (str): Current working directory of the instance
        message (str): Commit message

    """

    def run(self):
        """
        Saves the project by pushing to a remote repository

        Throws
        -------
        Exception if error occurs when running git add/commit/push
        """
        self.base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
        self.cwd = os.getcwd()
        self.git = Git()
        if self.options['message']:
            self.message = self.options['message']
        else:
            logging.info("No save message provided, defaulting to: Update")
            self.message = "Update"
        try:
            self.git.add(self.cwd)
            self.git.commit(self.message, self.cwd)
            self.git.push(self.cwd)
            logging.info("Successfully saved updates")
        except ValueError as err:
            logging.error(err)
        except Exception as err:
            logging.error(err)

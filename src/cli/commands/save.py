'''
Saves the project
'''

from .base import Base
import os
import sys
from shutil import copyfile
import logging
import subprocess
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)) + "/../modules")
from gitwrapper import Git


# Set up logger
FORMAT = 'carme: [%(levelname)s] %(message)s'
logging.basicConfig(level=logging.INFO, format=FORMAT)

class Save(Base):
    def run(self):
        # Get this scripts dir
        self.base_dir=os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
        self.cwd=os.getcwd()
        self.git = Git()
        if(self.options['message']):
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
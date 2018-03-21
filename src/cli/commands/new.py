'''
Creates a new project
'''

import os
import logging
from shutil import copyfile
from .base import Base
from ...modules.gitwrapper import Git

# Set up logger
FORMAT = 'carme: [%(levelname)s] %(message)s'
logging.basicConfig(level=logging.INFO, format=FORMAT)

class New(Base):
    """
    CLI command for creating a new carme project environment

    Attributes:
        git (object): Wrapper for git commands
        project_dir (str): Directory to the project
        project_name (str): Name of the project

    """

    def create_structure(self):
        """
        Creates a new directory structure of the project

        Throws
        -------
        OSError if error occurs when creating the structure
        """

        logging.info('Creating new project structure for %s', self.project_name)
        try:
            os.mkdir('apps')
            os.mkdir('data')
            os.mkdir('docker')
            os.mkdir('docker/pip-cache')
            os.mkdir('notebooks')
            copyfile(self.docker_dir + '/docker-compose.yaml', self.project_dir + \
                '/docker/docker-compose.yaml')
            config_file = open('config.yaml', 'w+')
            config_file.writelines('project_name: ' + self.project_name + '\n')
        except OSError as err:
            logging.error("Error creating the project structure")
            logging.error(err)

    def run(self):
        """
        Sets up a new carme project environment

        Throws
        -------
        Exception if error occurs when running git init
        """

        self.git = Git()
        if self.options['<project>'] == '.':
            self.project_dir = self.cwd
            self.project_name = input("Please enter project name: ")
            if not self.project_name:
                logging.error("Project name not entered. Please see carme --help")
            else:
                self.create_structure()
        else:
            if self.options['<project>']:
                self.project_name = self.options['<project>']
                self.project_dir = os.path.join(os.getcwd(), self.project_name)
            else:
                logging.error('Project name not supplied. See carme --help')
            if os.path.isdir(self.project_dir):
                logging.error('Project folder %s already exists', self.project_name)
            else:
                os.mkdir(self.project_dir)
                os.chdir(self.project_dir)
                self.create_structure()
                try:
                    self.git.init(self.project_dir)
                except Exception as err:
                    logging.error(err)

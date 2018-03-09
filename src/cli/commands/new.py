'''
Creates a new project
'''

from .base import Base
import os
import sys
from shutil import copyfile
import logging
import subprocess
from .git import Git

# Set up logger
FORMAT = 'carme: [%(levelname)s] %(message)s'
logging.basicConfig(level=logging.INFO, format=FORMAT)

class New(Base):
    def create_structure(self):
        # Create new project directory structure
        logging.info('Creating new project structure for ' + self.project_name)
        try:
            os.mkdir('apps')
            os.mkdir('data')
            os.mkdir('docker')
            os.mkdir('docker/pip-cache')
            os.mkdir('notebooks')
            copyfile(self.docker_dir + '/docker-compose.yaml', self.project_dir + '/docker/docker-compose.yaml')
            f= open('config.yaml','w+')
            f.writelines('project_name: ' + self.project_name + '\n')
            #f.writelines('packages:') Invalid
        except:
            logging.error("Error creating the project structure")
            logging.error(sys.exc_info()[0])


    def run(self):
        # Get this scripts dir
        self.git = Git()

        if(self.options['<project>'] == '.'):
            self.project_dir = self.cwd
            self.project_name = input("Please enter project name: ")
            if(self.project_name == False):
                logging.error("Project name not entered. Please see carme --help")
            else:
                self.create_structure()
        else:
            if(self.options['<project>']):
                self.project_name = self.options['<project>']
                self.project_dir = os.path.join(os.getcwd(), self.project_name)
            else:
                logging.error('Project name not supplied. See carme --help')
            if(os.path.isdir(self.project_dir)):
                logging.error('Project folder ' + self.project_name + ' already exists')
            else:
                os.mkdir(self.project_dir)
                os.chdir(self.project_dir)
                self.create_structure()
                try:
                    self.git.init(self.project_dir)
                except Exception as err:
                    logging.error(err)

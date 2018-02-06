'''
Creates a new project
'''

from .base import Base
import os
from shutil import copyfile
import logging

class New(Base):
    def run(self):
        # Set up logger
        FORMAT = 'carme: [%(levelname)s] %(message)s'
        logging.basicConfig(level=logging.INFO, format=FORMAT)

        # Get this scripts dir
        self.base_dir=os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
        self.docker_dir=os.path.dirname(self.base_dir)+'/data/docker'
        self.cwd=os.getcwd()

        if(self.options['<project>']):
            self.project_name = self.options['<project>']
            self.project_dir = os.getcwd() + '/' + self.project_name
        else:
            logging.error('Project name not supplied. See carme --help')
        
        if(os.path.isdir(self.project_dir)):
            logging.error('Project already exists with give name: ' + self.project_name)
        else:
            # Create new project structure
            logging.info('Creating new project structure for ' + self.project_name)
            os.mkdir(self.project_dir)
            os.chdir(self.project_dir)
            os.mkdir('dags')
            os.mkdir('data')
            os.mkdir('docker')
            os.mkdir('notebooks')
            copyfile(self.docker_dir + '/docker-compose.yaml', self.project_dir + '/docker/docker-compose.yaml')
            f= open('config.yaml','w+')
            f.writelines('project_name: ' + self.project_name + '\n')
            f.writelines('packages:')
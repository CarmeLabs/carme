'''
Creates a new project
'''

import click
import os
import sys
from shutil import copyfile
import logging
import subprocess
from ...modules.git import Git
from .base import DOCKER_DIR

# Set up logger
FORMAT = 'carme: [%(levelname)s] %(message)s'
logging.basicConfig(level=logging.INFO, format=FORMAT)


@click.command()
@click.argument('project_dir', type=click.Path(exists=False))
def new(project_dir):
    git = Git()
    project_name = os.path.basename(project_dir)

    def create_structure():
        # Create new project directory structure
        logging.info('Creating new project structure at ' + project_dir)
        try:
            os.mkdir('apps')
            os.mkdir('data')
            os.mkdir('docker')
            os.mkdir('docker/pip-cache')
            os.mkdir('notebooks')
            copyfile(os.path.join(DOCKER_DIR, 'docker-compose.yaml'), os.path.join(project_dir, 'docker/docker-compose.yaml'))
            f= open('config.yaml','w+')
            f.writelines('project_name: ' + project_name + '\n')
            #f.writelines('packages:') Invalid
        except:
            logging.error("Error creating the project structure")
            logging.error(sys.exc_info()[0])


    def run():
        os.mkdir(project_dir)
        os.chdir(project_dir)
        create_structure()
        try:
            git.init(project_dir)
        except Exception as err:
            logging.error(err)
    
    # call run
    run()

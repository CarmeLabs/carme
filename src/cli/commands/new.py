'''
Creates a new project
'''

import os
import logging
import click
from shutil import copyfile
from ...modules.gitwrapper import Git
from .base import DOCKER_DIR

# Set up logger
FORMAT = 'carme: [%(levelname)s] %(message)s'
logging.basicConfig(level=logging.INFO, format=FORMAT)

@click.command()
@click.argument('project_dir', type=click.Path())
def new(project_dir):
    """
    Creates a new carme project in project_dir or the given folder.
    """
    git = Git()
    project_name = os.path.basename(project_dir)
    project_dir = os.path.abspath(project_dir)

    if os.path.exists(project_dir):
        logging.warning(project_dir + " already exists!")
        return

    """
    Run the actual command
    """
    os.mkdir(project_dir)
    os.chdir(project_dir)

    logging.info('Creating new project structure at ' + project_dir)
    try:
        os.mkdir('apps')
        os.mkdir('data')
        os.mkdir('docker')
        os.mkdir('docker/pip-cache')
        os.mkdir('notebooks')
        copyfile(os.path.join(DOCKER_DIR, 'docker-compose.yaml'), os.path.join(project_dir, 'docker/docker-compose.yaml'))
        f = open('carme-config.yaml','w+')
        f.writelines('project_name: ' + project_name + '\n')
        #f.writelines('packages:') Invalid

    except Exception as err:
        logging.error("Error creating the project structure")
        logging.error(err)

    try:
        git.init(project_dir)
    except Exception as err:
        logging.error(err)

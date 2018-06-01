'''
Creates a new project
'''

import os
import logging
import click
from shutil import copyfile, copytree
from ...modules.gitwrapper import Git
from .base import  setup_logger, DEFAULT_DIR,CONFIG_DIR
from .connect import _connect

# Set up logger
setup_logger()

@click.command()
@click.argument('project_dir', type=click.Path())
@click.option('--image', default="base", help='The Jupyter docker image.')
def new(project_dir, image):
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
    logging.info(DEFAULT_DIR)
    logging.info('Creating new project structure at ' + project_dir)
    try:
        for dir in DEFAULT_DIR:
            os.mkdir(dir)

        with open('docker-compose.yaml', 'w+') as f:
            f.writelines('version: \'3\'\n\n')
            f.writelines('networks:\n')
            f.writelines('  carme-net:\n')
            f.writelines('    external:true\n')
        with open('.carmeignore', 'w+') as f:
            f.writelines('packages\n')
            f.writelines('.git\n')
        os.chdir(CONFIG_DIR)
        with open('carme-config.yaml','w+') as f:
            f.writelines('project:\n')
            f.writelines('  name: ' + project_name + '\n')
            f.writelines('  repository: ')
    except Exception as err:
        logging.error("Error creating the project structure")
        logging.error(err)

    try:
        git.init(project_dir)
    except Exception as err:
        logging.error(err)

    validResponse = False
    while not validResponse:
        connectDecision = input("Would you like to connect to a git repository? (y/n): ")
        if connectDecision.lower() == 'y':
            _connect()
            validResponse = True
        elif connectDecision.lower() == 'n':
            logging.info("Git repository not set. Changes will only be saved locally.")
            logging.info("To connect to git repository, run `carme connect`")
            validResponse = True
        else:
            logging.info("Invalid response. Please enter 'y' or 'n'")

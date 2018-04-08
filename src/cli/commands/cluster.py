'''
Creates a new project
'''

import os
import logging
import click
from shutil import copyfile
from ...modules.gitwrapper import Git
from .base import *
from .clusters.azure import *
from .clusters.gcp import *
SUPPORTED=['gcp','azure']

setup_logger()

@click.command()
#@click.argument('cloud', default=False, help='Run Docker container in the background.')
@click.option('--dryrun', is_flag=True, default=False, help='Just the command without executing.')


def cluster(dryrun):
    """
    Can be used to create a manage a Kubernetes cluster.
    """
    ROOT_DIR=get_project_root()
    kwargs=get_config(ROOT_DIR)
    try:
        print(kwargs,dryrun)
        # os.mkdir('apps')
        # os.mkdir('data')
        # os.mkdir('docker')
        # os.mkdir('docker/pip-cache')
        # os.mkdir('notebooks')
        # copyfile(os.path.join(DOCKER_DIR, 'docker-compose.yaml'), os.path.join(project_dir, 'docker/docker-compose.yaml'))
        # copytree(os.path.join(DOCKER_DIR,image), os.path.join(project_dir, 'docker/'+image))
        # os.rename(os.path.join(project_dir, 'docker/'+image),os.path.join(project_dir, 'docker/jupyter'))
        # with open('carme-config.yaml','w+') as f:
        #     f.writelines('project_name: ' + project_name + '\n')
        #     f.writelines('jupyter_image: carme/' + image + '\n')

    except Exception as err:
        logging.error("Error creating the project structure")
        logging.error(err)

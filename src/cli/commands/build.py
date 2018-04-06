'''
Builds images
'''

import os
import logging
import click
from shutil import copyfile
from .base import bash_command, get_project_root, setup_logger, load_yaml

# Set up logger
setup_logger()

@click.command()
#TBD Build all images in the docker
#TBD Build and push.

def build():
    """
    Launch Jupyter lab.
    """
    ROOT_DIR=get_project_root()
    kwargs=load_yaml(os.path.join(ROOT_DIR, 'carme-config.yaml'))
    print(kwargs['jupyter_image'])
    cmd='docker build -t '+kwargs['jupyter_image']+':latest -t carme/'+kwargs['project_name']+':latest -t carme/jupyter:latest '+os.path.join(ROOT_DIR, 'docker/jupyter')
    bash_command("Building Jupyter",cmd)

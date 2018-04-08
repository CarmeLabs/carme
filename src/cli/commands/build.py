'''
Builds images.
'''

import os
import logging
import click
from shutil import copyfile
from .base import *

# Set up logger
setup_logger()

@click.command()
@click.option('--force', is_flag=True, default=False, help='Force full rebuild without using cache.')

#TBD Build all images in the docker repository.
#TBD Build and push.

def build(force):
    """
    Build project docker images.
    """
    if force:
        docop=' --no-cache '
    else:
        docop=''
    ROOT_DIR=get_project_root()
    kwargs=get_config(ROOT_DIR)
    cmd='docker build '+docop+'-t '+kwargs['jupyter_image']+':latest -t carme/'+kwargs['project_name']+':latest -t carme/jupyter:latest '+os.path.join(ROOT_DIR, 'docker/jupyter')
    bash_command("Building Jupyter", cmd)

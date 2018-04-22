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
@click.option('--push', is_flag=True, default=False, help='Push image to Dockerhub (must be logged-in).')
@click.option('--jupyterhub', is_flag=True, default=False, help='Update Jupyterhub')

#TBD Build all images in the docker repository.
#TBD Build and push.

def build(force, push, jupyterhub):
    """
    Build project docker images.
    """
    if force:
        docop=' --no-cache '
    else:
        docop=''
    ROOT_DIR=get_project_root()
    kwargs=get_config(ROOT_DIR)
    tag= bash_command("Get the current hash.", 'git log -1 --format=%h')
    print("tag", tag)

    #Build Jupyter
    cmd='docker build '+docop+'-t '+kwargs['jupyter_image']+':latest -t '+kwargs['jupyter_image']+':$(git log -1 --format=%h) ' +  os.path.join(ROOT_DIR, 'docker/jupyter')
    
    bash_command("Building Jupyter", cmd)

    #Currently there is an issue where if the build fails it will still push.
    if push:
        cmd='docker push '+kwargs['jupyter_image']+':latest'
        bash_command("Pushing to Dockerhub", cmd)
        cmd='docker push '+kwargs['jupyter_image']+':$(git log -1 --format=%h)'
        bash_command("Pushing to Dockerhub", cmd)

    if jupyterhub:
        #This should update the singleuser tag
        # in /app/jupyterhub/config.yaml
        print("tbd")

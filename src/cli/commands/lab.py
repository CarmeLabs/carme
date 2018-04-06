'''
Launches an instance of JupyterLab.
'''

import os
import logging
import click
from shutil import copyfile
from .base import bash_command, get_project_root, setup_logger

# Set up logger
setup_logger()

@click.command()
@click.option('--image', default="carme/jupyter:latest", help='The Jupyter docker image to be launched.')
@click.option('--background', is_flag=True, default=False, help='Run docker container in the background.')

def lab(image, background):
    """
    Launch JupyterLab (using docker).
    """
    if background:
        flags = '-d'
    else:
        flags = '-ti --rm'

    cwd=os.getcwd()
    cmd='docker run '+flags+' -p 8888:8888  -v '+ cwd+ ':/home/jovyan/work '+image+' start.sh jupyter lab'
    bash_command("Launching JupyterLab", cmd)

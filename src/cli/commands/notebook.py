'''
Launches an instance of Jupyter notebook.
'''

import os
import logging
import click
from shutil import copyfile
from .base import bash_command, get_project_root, setup_logger

# Set up logger
setup_logger()

@click.command()
@click.option('--image', default="carme/jupyter:latest", help='The Jupyter docker image (must be based on Jupyter stacks).')
@click.option('--background', is_flag=True, default=False, help='Run Docker container in the background.')
def notebook(image, background):
    """
    Launch Jupyter Notebook (using Docker).
    """
    if background:
        flags = '-d'
    else:
        flags = '-ti --rm'
    cwd=os.getcwd()
    cmd='docker run '+flags+' -p 8888:8888  -v '+ cwd+ ':/home/jovyan/work '+image
    bash_command("Launching Jupyter Notebook", cmd)

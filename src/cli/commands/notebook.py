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
@click.option('--image', default="carme/jupyter:latest", help='The Jupyter docker image.')
def notebook(image):
    """
    Launch Jupyter Notebook (using docker).
    """
    cwd=os.getcwd()

    cmd='docker run -ti --rm -p 8888:8888  -v '+ cwd+ ':/home/jovyan/work '+image

    bash_command("Launching Jupyter Notebook",cmd)

    #print("cmd", cmd)

'''
Creates a new project
'''

import os
import logging
import click
from shutil import copyfile
from ...modules.gitwrapper import Git
from .base import bash_command, get_project_root

# Set up logger
FORMAT = 'carme: [%(levelname)s] %(message)s'
logging.basicConfig(level=logging.INFO, format=FORMAT)

@click.command()
#@click.argument('ima', type=click.Path())

def lab(image='carme/singleuser:latest'):
    """
    Launch Jupyter lab.
    """
    cwd=os.getcwd()

    cmd='docker run -p 8888:8888  -v '+ cwd+ ':/home/jovyan/work '+image+' start.sh jupyter lab'

    bash_command("Launching Jupyterlab",cmd)

    #print("cmd", cmd)

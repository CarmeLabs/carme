'''
Launches an instance of Jupyter notebook.
'''

import os
import logging
import click
from shutil import copyfile
from ...modules.base import *
from ...modules.dockerwrapper import service_create

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
    #cmd='docker run '+flags+' -p 8888:8888  -v '+ cwd+ ':/home/jovyan/work '+image
    #bash_command("Launching Jupyter Notebook", cmd)
    #TODO test this
    #The ports feild might be wrong? The documentation was strange about this.
    service_create(image, name="notebook", ports={'8888':8888}, mounts=[cwd+":/home/jovyan/work"])

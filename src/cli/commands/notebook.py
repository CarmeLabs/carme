'''
Launches default instance of Jupyter notebook. Image used is (1) specified in command, (2) set in <current-project>/config/carme-config.yaml,
or (3) set in /<home>/.carme/config/carme-config.yaml
'''

import os
import logging
import click
from shutil import copyfile
from ...modules.base import setup_logger, JUPYTER_IMAGE_KEY, CONFIG_FILE, CWD, bash_command
from ...modules.notebookwrapper import get_flags, get_image_port
from pathlib import Path

# Set up logger
setup_logger()


@click.command()
@click.option('--image', help='The Jupyter docker image (must be based on Jupyter stacks).')
@click.option('--port', help='The Jupyter docker image (must be based on Jupyter stacks).')
@click.option('--background', is_flag=True, default=False, help='Run Docker container in the background.')
@click.option('--dryrun', is_flag=True, default=False, help='Only print the command, do not run.')
def notebook(image, port, background, dryrun):
    """
    Launch Jupyter Notebook (using Docker).
    """
    # TODO Clean this up a bit.
    image, port = get_image_port(image, port)
    flags = get_flags(background)
    if image is None:
        logging.error("Set the key "+JUPYTER_IMAGE_KEY +
                      "in the project or /<home>/.carme/config/"+CONFIG_FILE+" to use this command.")
        quit()
    else:
        logging.info("Launching the Jupyter Image: "+image)
    #print("flags", flags, "port",port)
    cmd = 'docker run '+flags+' -p '+port + \
        ':8888  -v '+CWD+':/home/jovyan/work '+image
    if dryrun:
        logging.info("Values: " + cmd)
    else:
        bash_command("Launch Notebook", cmd)

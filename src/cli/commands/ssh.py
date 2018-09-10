'''
Provision a docker container and mount the current working directory inside it
'''
import os
import click
import logging
from subprocess import call
from ...modules.base import *
# from ...modules.dockerwrapper import service_create

# Set up logger
setup_logger()

@click.command()
@click.argument('image')
@click.option('--dest', is_flag=False, default='/carme_workspace', help='Absolute path to the directory on the container where the current working directory will be mounted')
@click.option('--rm', is_flag=True, default=True, help='Whether or not the container will be removed when the user exits')

def ssh(image, dest, rm):
    """
    Provision a docker container and mount the current working directory inside it
    """

    # Captures the current working directory to be mounted inside the container
    workdir = os.getcwd()

    # Defines value for the `docker run -v` flag
    volume = workdir + ':' + dest

    # Starts the docker container
    if rm:
        proc = call(["docker", "run", "--rm", "-it", "-v", volume, image])
    else:
        proc = call(["docker", "run", "-it", "-v", volume, image])

    # TODO - we'll likely want to introduce some error handling here
    return True
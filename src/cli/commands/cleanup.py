'''
Delete and remove all images.
'''
import os
import logging
import click
from ...modules.base import *
# Set up logger
setup_logger()
@click.command()
def cleanup():
    """
    Delete and remove all images.
    """
    cmd='docker rmi --force  $(docker images -a -q)'
    bash_command("Deleting all images", cmd)

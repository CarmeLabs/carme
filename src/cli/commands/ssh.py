'''
Spin up docker container and mount current directory.
'''
import os
import logging
import click
from ...modules.base import *
# Set up logger
setup_logger()

@click.command()
# @click.option('--remove', is_flag=True, default=False, help='Remove all images.')

def ssh():
    """
    Spin up docker container and mount current directory.
    """
    # if remove:
    #     cmd='docker-compose down'
    # else:
    #     cmd='docker-compose stop'
    print('RUN CARME SSH HERE')
    # project_root=get_project_root()
    # os.chdir(project_root)
    # bash_command("Stopping containers", cmd)

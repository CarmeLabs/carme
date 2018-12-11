'''
Launch all installed applications.
'''
import os
import logging
import click
from ...modules.base import setup_logger, get_project_root, bash_command
# Set up logger
setup_logger()


@click.command()
@click.option('--remove', is_flag=True, default=False, help='Remove all images.')
def stop(remove):
    """
    Stop (and optionally remove, --remove) all containers running in background.
    """
    if remove:
        cmd = 'docker-compose down'
    else:
        cmd = 'docker-compose stop'

    project_root = get_project_root()
    os.chdir(project_root)
    bash_command("Stopping containers", cmd)

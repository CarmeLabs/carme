'''
Launch all installed applications.
'''
import os
import logging
import click
from ...modules.base import *
# Set up logger
setup_logger()

@click.command()
@click.option('--background', is_flag=True, default=False, help='Run Docker-compose up in the background.')
def start( background):
    """
    Launch all installed applications.
    """
    if background:
        flags = '-d'
    else:
        flags = ' '
    project_root=get_project_root()
    os.chdir(project_root)

    cmd='docker-compose -f docker-compose.yaml up '+flags
    bash_command("Launching all applications", cmd)

'''
Creates a new project
'''
import os
import logging
import click
from shutil import copyfile, copytree
from ...modules.packager import Packager, create_package
from ...modules.base import *
from ...modules.yamltools import *
from .git import _git

# Set up logger
setup_logger()

@click.command()
@click.argument('project_dir', type=click.Path())
@click.option('--package', default="default", help='Enter the package for initial project scaffold.')
@click.option('--git', is_flag=True, default=False, help='Initialize a git repository.')

def new(project_dir, package, git):
    """
    Creates a new carme project in project_dir or the given folder.
    """

    project_name = os.path.basename(project_dir)
    project_dir = os.path.abspath(project_dir)

    if os.path.exists(project_dir):
        logging.warning(project_dir + " already exists!")
        return

    """
    Run the actual command
    """
    os.mkdir(project_dir)
    os.chdir(project_dir)
    logging.info("Installing using package: "+package)
    Packager(package, project_dir).install()
    update_key('project_name', project_name, os.path.join(project_dir, CONFIG_DIR, CONFIG_FILE))

    #The git flag will connect a github repository.
    if git:
        _git()
    else:
        logging.info("Git repository not set. Changes will only be saved locally.")
        logging.info("To connect to git repository, run `carme git`")

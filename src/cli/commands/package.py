"""
Manage project packages
"""

import logging
import click
from ...modules.packager import Packager, create_package
from ...modules.gitwrapper import Git
from .base import *
import validators


# Set up logger
setup_logger()

@click.group()
def package():
    """
    Manage packages on the project.
    """
    pass

@package.command()
@click.argument('package_path')
def install(package_path):
    """
    Install a package into the project.
    """
    logging.info("Installing package: " + package_path)

    #Get the path for core packages
    tmp_path=os.path.join(DATA_DIR, "packages", package_path,"package","latest.zip")
    if os.path.exists(tmp_path):
        logging.info("Installing cached core package.")
        package_path=tmp_path
        logging.info("Package location: " + package_path)
    #Install the package
    Packager(package_path, get_project_root()).install()

@package.command()
@click.argument('package_path')
def remove(package_path):
    """
    Remove a package from the project.
    """
    Packager(package_path, get_project_root()).remove()

@package.command()
@click.argument('package_path')
def download(package_path):
    """
    Download a package and cache it.
    """
    Packager(package_path, get_project_root()).download()

@package.command()
#@click.option('--archive', is_flag=True, default=False, help='Create an archive of the work.')
def create():
    """
    Create a package from the current project directory.
    """
    #Get the project root
    project_root=get_project_root()
    #TO DO Create process to flag archived version/otherwise delete
    #create_package(project_root, archive)
    create_package(project_root)

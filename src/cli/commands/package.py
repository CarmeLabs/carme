"""
Manage project packages
"""

import logging
import click
from ...modules.packager import Packager
from .base import get_project_root

# Set up logger
FORMAT = 'carme: [%(levelname)s] %(message)s'
logging.basicConfig(level=logging.INFO, format=FORMAT)

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
    logging.info("Installing package from: " + package_path)
    Packager(package_path, get_project_root()).install()

@package.command()
@click.argument('package_path')
def remove(package_path):
    """
    Remove a package from the project.
    """
    Packager(package_path, get_project_root()).install()

@package.command()
@click.argument('package_path')
def download(package_path):
    """
    Download a package and cache it.
    """
    Packager(package_path, get_project_root()).install()

"""
Manage project packages
"""

import click
from ...modules.packager import Packager
import logging

# Set up logger
FORMAT = 'carme: [%(levelname)s] %(message)s'
logging.basicConfig(level=logging.INFO, format=FORMAT)

@click.group()
def package():
    pass

@package.command()
@pacakge.arguments('package_path')
def install(package_path, project_dir):
    logging.info("Installing package from: " + package_path)
    Packager(package_path, project_dir).install()
    
@package.command()
@pacakge.arguments('package_path')
def remove(package_path, project_dir):
    Packager(package_path, project_dir).install()

@package.command()
@pacakge.arguments('package_path')
def download(package_path, project_dir):
    Packager(package_path, project_dir).install()

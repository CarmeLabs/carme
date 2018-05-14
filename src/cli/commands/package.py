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
def create():
    """
    Create a package from the current project directory.
    """
    #Get the project root
    project_root=get_project_root()
    #Get the project location
    package_path=os.path.join(project_root,"package","latest.zip")
    #Loads the configuration in the root directory.
    kwargs=get_config(project_root)
    #This requires a git commit
    git = Git()
    #TBD Check for uncommitted changes require commit before packaging.
    #git.check_changes()
    #TBD get the git commit hash (short version).
    out=git.log(1, ['--format=%h'])
    logging.info(out)
    #get the current timestamp
    kwargs['package_created']="today"   #TBD
    kwargs['commit']="7a7d2"  #TBD
    #Update the config-yaml file.
    update_yaml(kwargs)
    #Create the package. #TBD
    create_package(package_path, project_root)

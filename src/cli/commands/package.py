'''
Manage project packages
'''

import logging
import click
import re
from ...modules.packager import Packager
from ...modules.gitwrapper import Git
from ...modules.base import *
from ...modules.yamltools import *
from time import strftime, localtime
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
@click.option('--index', is_flag=True, default=False, help='Update the default index.')
def create(index):
    """
    Create a package from the current project directory.
    """
    #Get the project root
    project_root=get_project_root()
    current_time=strftime("%Y%m%d_%H%M%S", localtime())
    logging.info("Creating package for current project." )
    package_name=os.path.basename(project_root)
    filename=package_name+"_"+current_time+".zip"
    package_path=os.path.join(project_root,PACKAGES_DIR,filename)
    logging.info("Creating package for current project: "+package_path )
    Packager(package_path, get_project_root(),True).create()

    if index:
        os.chdir(project_root)
        index=os.path.join(os.pardir, DEFAULT_DIR, CONFIG_DIR, INDEX_FILE)
        kwargs=load_yaml_file(index)
        if package_name in kwargs:
            kwargs[package_name]=re.sub(r'\d\d\d\d\d\d\d\d_\d\d\d\d\d\d',current_time, kwargs[package_name])
            logging.info("Updating index: " + kwargs[package_name])
        else:
            kwargs[package_name]=kwargs['default']
            kwargs[package_name]=kwargs[package_name].replace('default', package_name)
            kwargs[package_name]=re.sub(r'\d\d\d\d\d\d\d\d_\d\d\d\d\d\d',current_time, kwargs[package_name])
            logging.info("Creating index: " + kwargs[package_name])
        update_yaml_file(index, kwargs)


    #create_package(project_root)

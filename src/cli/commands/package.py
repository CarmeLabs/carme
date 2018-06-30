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
    project_root=get_project_root()
    #Update the package short name to url using index.
    package_path=_install_package(project_root, package_path)


def _install_package(project_root, package):
    """
    Updated the package url from the package name.
    @return: The url or the origional name.
    """
    #See if there is a different index set.
    config_file=os.path.join(project_root, CONFIG_DIR, CONFIG_FILE)
    if os.path.exists(config_file):
        kwargs=load_yaml_file(config_file)
        index=kwargs['package_index']
        logging.info("Using package_index set in carme-config.yaml : "+index)

    else:
        index=PACKAGE_INDEX
    index=load_yaml_url(index)
    if package in index:
        package=index[package]

    #Some packages can be install multiple packages.
    if isinstance(package, ruamel.yaml.comments.CommentedSeq):
        logging.info('Looping through multiple package installs:'+command+ ':')
        #for x in package:
        #    logging.info('Looping through multiple packages, installing: '+x)
    else:
        logging.info("Downloading from: "+package)
        Packager(package, project_root).install()
    return package

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
    Packager(package_path, get_project_root()).create()

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

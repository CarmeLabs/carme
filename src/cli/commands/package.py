'''
Manage project packages
'''

import logging
import click

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
def list():
    """
    List all of the available packages.
    """
    project_root=get_project_root()
    config_file=os.path.join(project_root, CONFIG_DIR, CONFIG_FILE)
    if os.path.exists(config_file):
        kwargs=load_yaml_file(config_file)
        if PACKAGE_INDEX_KEY in kwargs:
            packages=load_yaml_url(kwargs[PACKAGE_INDEX_KEY])
        #Should update and look in .carme/config
        else:
            packages=load_yaml_url(PACKAGE_INDEX)

    ruamel.yaml.dump(packages, sys.stdout, Dumper=ruamel.yaml.RoundTripDumper)

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

    package=_return_package_url(project_root,package)

    #Some packages can be install multiple packages.
    if isinstance(package, ruamel.yaml.comments.CommentedSeq):
        #Loop through packages
        for x in package:
            logging.info('Multiple packages, installing: '+x)
            x_url=_return_package_url(project_root, str(x))
            print("xurl",x_url)
            #Packager(x_url, project_root).install()
    else:
        logging.info("Downloading from: "+str(package))
        Packager(package, project_root).install()
    return package

# @package.command()
# @click.argument('package_path')
# def remove(package_path):
#     """
#     Remove a package from the project.
#     """
#     Packager(package_path, get_project_root()).remove()
#
# @package.command()
# @click.argument('package_path')
# def download(package_path):
#     """
#     Download a package and cache it.
#     """
#     Packager(package_path, get_project_root()).download()

@package.command()
@click.option('--index', is_flag=True, default=False, help='Update the default index.')
def create(index):
    """
    Create a package from the current project directory.
    """
    #Get the project root
    project_root=get_project_root()
    package_name=os.path.basename(project_root)
    logging.info("Creating package for current project: "+ package_name)
    Packager(package_name, project_root).create(index)

def _return_package_url(project_root,package):
    #See if there is a different index set.
    config_file=os.path.join(project_root, CONFIG_DIR, CONFIG_FILE)
    if os.path.exists(config_file):
        kwargs=load_yaml_file(config_file)
        index_url=kwargs['package_index']
        logging.info("Using package_index set in carme-config.yaml : "+index_url)
    else:
        index_url=PACKAGE_INDEX
    index=load_yaml_url(index_url)
    if package in index:
        package=index[package]
        return package
    elif package[0:4]=='http':
        return package
    else:
        logging.error("The package "+package+" was neither a valid url or contained in the index: "+index_url)
        exit()
    #create_package(project_root)

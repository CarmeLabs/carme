'''
Git Helper.
'''

import click
import os
from ruamel.yaml import YAML
import logging
import subprocess
import validators
from .base import *
from ...modules.gitwrapper import Git

# Set up logger
FORMAT = 'carme: [%(levelname)s] %(message)s'
logging.basicConfig(level=logging.INFO, format=FORMAT)

@click.command()
def remote():
    _git_remote()

def _git_init(project_dir):
    gitobj = Git()
    try:
        gitobj.init(project_dir)
        logging.info("Initialized git repository in project.")
    except Exception as err:
        logging.error(err)

def _git_remote(project_dir):
    """
    Connects to the github repo.
    """
    # Get this scripts dir
    cwd=os.getcwd()
    git = Git()
    yaml=YAML()
    remoteRepo = input("Enter remote git repository URL: ")
    if(validators.url(remoteRepo)):
        try:
            git.remote_add(project_dir, remoteRepo)
            # with open(CONFIG_FILE) as f:
            #     yamlData = yaml.load(f)
            #     for item in yamlData:
            #         if item == 'project':
            #             yamlData[item]['repository'] = remoteRepo
            # with open(CONFIG_FILE, "w") as f:
            #     yaml.dump(yamlData, f)
            logging.info("Successfully connected project to " + remoteRepo)
        except Exception as err:
            logging.error(err)
    else:
        logging.error("Invalid URL. Please see carme --help")

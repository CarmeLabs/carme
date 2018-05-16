'''
Connects to the github repo
'''

import click
import os
from ruamel.yaml import YAML
import logging
import subprocess
import validators
from ...modules.gitwrapper import Git

# Set up logger
FORMAT = 'carme: [%(levelname)s] %(message)s'
logging.basicConfig(level=logging.INFO, format=FORMAT)

@click.command()
def connect():
    _connect()

def _connect():
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
            git.remote_add(cwd, remoteRepo)
            with open("carme-config.yaml") as f:
                yamlData = yaml.load(f) 
                for item in yamlData:
                    if item == 'project':
                        yamlData[item]['repository'] = remoteRepo
            with open("carme-config.yaml", "w") as f:
                yaml.dump(yamlData, f)
            logging.info("Successfully connected project to " + remoteRepo)
        except Exception as err:
            logging.error(err)
    else:
        logging.error("Invalid URL. Please see carme --help")

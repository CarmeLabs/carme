'''
Connects to the github repo
'''

import click
import os
import logging
import subprocess
import validators
from ...modules.gitwrapper import Git

# Set up logger
FORMAT = 'carme: [%(levelname)s] %(message)s'
logging.basicConfig(level=logging.INFO, format=FORMAT)

@click.command()
def connect():
    """
    Connects to the github repo.
    """
    # Get this scripts dir
    cwd=os.getcwd()
    git = Git()
    remote_repo = input("Enter remote git repository URL: ")
    if(validators.url(remote_repo)):
        try:
            git.remote_add(cwd, remote_repo)
            logging.info("Successfully connected project to " + remote_repo)
        except Exception as err:
            logging.error(err)
    else:
        logging.error("Invalid URL. Please see carme --help")

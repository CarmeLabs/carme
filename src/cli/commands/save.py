'''
Saves the project
'''

from .base import BASE_DIR
import os
import logging
import subprocess
import click
from ...modules.gitwrapper import Git


# Set up logger
FORMAT = 'carme: [%(levelname)s] %(message)s'
logging.basicConfig(level=logging.INFO, format=FORMAT)

@click.command()
@click.argument('message')
def save(message):
    """
    A simler alias to git commit and push.
    """
    # Get this scripts dir
    cwd = os.getcwd()
    git = Git()
    if not message:
        logging.info("No save message provided, defaulting to: Update")
        message = "Update"
    try:
        git.add(cwd)
        git.commit(message, cwd)
        git.push(cwd)
        logging.info("Successfully saved updates")
    except ValueError as err:
        logging.error(err)
    except Exception as err:
        logging.error(err)

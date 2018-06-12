'''
Saves the project
'''

import click
from .git import _git_save
from ...modules.base import *
SAVE_DEFAULT= "Carme Saved Executed."
SAVE_HELP = "Use message to record changes made.  This will be stored in git with the commit."

# Set up logger
setup_logger()
@click.command()
@click.option('--message', default=SAVE_DEFAULT, help=SAVE_HELP)
def save(message):
    """
    A simler alias to git commit and push.
    """
    _git_save()
    #TBD Add functionality to push data to bucket.

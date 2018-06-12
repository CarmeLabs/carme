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
@click.option('--nopush', is_flag=True, default=False, help="Don't push to the remote repository")
def save(message):
    """
    A simler alias to git commit and push.
    """
    _git_save(message)
    if nopush:
        logging.info("Use carme save --push to push changes")
    else:
        _git_push()
    #TBD Add functionality to push data to bucket.

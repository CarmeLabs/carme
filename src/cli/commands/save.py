'''
Saves the project
'''

import os
import click
import logging
from .git import _git_save, _git, _git_push
from ...modules.base import setup_logger, get_project_root
SAVE_DEFAULT = "Carme Saved Executed."
SAVE_HELP = "Use message to record changes made.  This will be stored in git with the commit."

# Set up logger
setup_logger()


@click.command()
@click.option('--message', default=SAVE_DEFAULT, help=SAVE_HELP)
@click.option('--push', is_flag=True, default=False, help="Don't push to the remote repository")
def save(message, push):
    """
    A simler alias to git commit and push.
    """
    logging.info("Checking for git")
    project_root = get_project_root()
    if not os.path.isdir(os.path.join(project_root, '.git')):
        print(os.path.join(project_root, '.git'))
        logging.info("Git not initiated in project. Doing that now.")
        _git()

    _git_save(message)
    if push:
        _git_push()
    else:
        logging.info("Use carme save --push to push changes")

    # TBD Add functionality to push data to bucket.

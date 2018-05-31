'''
Saves the project
'''

from .base import BASE_DIR
import os
import logging
import subprocess
import click
from ...modules.gitwrapper import Git
save_default_message= "No save message provided, defaulting to: `Carme Saved Executed`."
save_help = "Use message to record changes made.  This will be stored in git with the commit."

# Set up logger
FORMAT = 'carme: [%(levelname)s] %(message)s'
logging.basicConfig(level=logging.INFO, format=FORMAT)

@click.command()
@click.option('--message', default=save_default_message, help=save_help)
def save(message):
    """
    A simler alias to git commit and push if there is a remote.
    """
    # Get this scripts dir
    cwd = os.getcwd()
    git = Git()

    try:
        result= git.add(cwd)
        print("git add",result)
        git.commit(message, cwd)

    #    git.push(cwd) Removing push.
        logging.info("Successfully saved updates")
    except ValueError as err:
        logging.error(err)
    except Exception as err:
        logging.error(err)

    #Ideally this would check the remote and then push only if there is a remoteself.
    #If there isn't a remote it should warn the user but should just save.
    remote=git.check_remote()
    print('result',remote)
    #TBD Check for remote and only push if remote exists.

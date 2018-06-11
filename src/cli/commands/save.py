'''
Saves the project
'''

from .base import BASE_DIR
import os
import logging
import subprocess
import click
#import yaml #JNK need to add to dependencies. 
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
        pushed = False
        with open("carme-config.yaml") as f:
                yamlData = yaml.load(f)
                for item in yamlData:
                    if item == 'project':
                        if yamlData[item]['repository'] != None:
                            git.push(cwd)
                            pushed = True
        if not pushed:
            logging.warning("No git repository set. Changes only saved locally.")
        else:
            logging.info("Successfully saved updates")
    except ValueError as err:
        logging.error(err)
    except Exception as err:
        logging.error(err)

'''
Git Helper.
'''
import click
import os
from ruamel.yaml import YAML
import logging
import subprocess
import validators
from ...modules.base import *
from ...modules.yamltools import *

# Set up logger
FORMAT = 'carme: [%(levelname)s] %(message)s'
logging.basicConfig(level=logging.INFO, format=FORMAT)

@click.command()
def git():
    _git()

def _git():
    project_dir=get_project_root()
    _git_init(project_dir)
    _git_remote(get_project_root())
    #_git_initial_push()

def _git_init(project_dir):
    bash_command("git init", "git init")

def _git_initial_push():
    bash_command("git push", "git push --set-upstream origin master")

def _git_save(message='Carme save executed'):
    bash_command("git add", "git add -A")
    bash_command("git commit", "git commit -m 'Carme Saved'")

def _git_push():
    bash_command("git push", "git push")

def _git_remote(project_dir):
    """
    Connects to the github repo.
    """
    os.path.join(CONFIG_DIR, 'carme-config.yaml')
    remoteRepo = input("Enter remote git repository URL: ")
    if(validators.url(remoteRepo)):
        #update_yaml(os.path.join(get_project_root(), CONFIG_FILE), 'repository', remoteRepo)
        kwargs=get_config()
        kwargs['repository']=remoteRepo
        update_config(kwargs)
        bash_command("Adding reposiotry","git remote add origin "+remoteRepo)
    else:
        logging.error("Invalid URL. Please see carme --help")

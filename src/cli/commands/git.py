'''
Launches an instance of JupyterLab.
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
#@click.option('--push', is_flag=True, default=False, help='Initialize a git repository.')
def git():
    """
    Initializes git and performs initial commit/push to GitHub.
    """
    _git()

def _git():
    project_root=get_project_root()
    print("current project",project_root)
    if not os.path.isdir(os.path.join(project_root, '.git')):
        _git_init(project_root)
        _git_remote(project_root)
        _git_save()
        _git_initial_push()

def _git_init(project_root):
    os.chdir(os.path.join(project_root))
    bash_command("git init", "git init")

def _git_initial_push():
    bash_command("git push", "git push -u origin master")

def _git_save(message='Carme save executed'):
    bash_command("git add", "git add -A")
    bash_command("git commit", "git commit -m 'Carme Saved'")

def _git_push():
    bash_command("git push", "git push")

def _git_remote(project_root):
    """
    Connects to the github repo.
    """
    remote = input("Enter remote git repository URL: ")
    if(validators.url(remote)):
        bash_command("Adding repository","git remote add origin "+remote)
        update_key('repository', remote, os.path.join(project_root, CONFIG_DIR, CONFIG_FILE))
    else:
        logging.error("Invalid URL. Please see carme --help")

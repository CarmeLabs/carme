"""
Variables and Functions used by multiple CLI commands
"""
import os
import subprocess
import logging
import ruamel.yaml
import urllib.request
from subprocess import call, DEVNULL, Popen
from os import path, pardir, getcwd
from .yamltools import *

# Global Constants
CLI_DIR = path.abspath(path.join(path.dirname(__file__), pardir))
BASE_DIR = path.dirname(CLI_DIR)
CONFIG_DIR = 'config'
COMMANDS_DIR = 'commands'
PACKAGES_DIR = 'packages'
DOCKER_DIR = 'docker'
CONFIG_FILE = 'carme-config.yaml'
INDEX_FILE = 'index.yaml'
DEFAULT_DIR = 'default'
APP_DIR = 'apps'
DATA_DIR = 'data'
CODE_DIR = 'code'
NOTEBOOKS_DIR = os.path.join(CODE_DIR, 'notebooks')
DOCS_DIR = 'docs'
SCRIPTS_DIR = os.path.join(CODE_DIR, 'scripts')

RST_DIR = os.path.join(DOCS_DIR, 'rst')
MERGE_LIST = ['./.carmeignore',
              './docker-compose.yaml', 'config/carme-config.yaml']
PACKAGE_INDEX = 'https://raw.githubusercontent.com/CarmeLabs/packages/master/default/config/index.yaml'
PACKAGE_INDEX_KEY = 'package_index'
JUPYTER_IMAGE_KEY = 'jupyter_image'
JUPYTER_PORT_KEY = 'jupyter_port'

CWD = getcwd()


def get_project_root():
    """
    Traverses up until it finds the folder with `.carmeignore` in it.
    @return: The absolute path to the project root or None if not in a project
    """
    cd = os.getcwd()
    while not os.path.exists(os.path.join(cd, ".carmeignore")):
        if cd == "/":
            return None
        cd = os.path.dirname(cd)
    #logging.info("Current project root: "+os.path.abspath(cd))
    return os.path.abspath(cd)


def setup_logger():
    """
    Sets up logging
    """
    FORMAT = 'carme: [%(levelname)s] %(message)s'
    logging.basicConfig(level=logging.INFO, format=FORMAT)


def bash_command(command, syntax, error="error"):
    try:
        print("Executing "+command+":\n", syntax)
        #result=subprocess.Popen([git, init], cwd=get_project_root())
        result = subprocess.call(syntax, shell=True, executable='/bin/bash')
        return result
    except subprocess.CalledProcessError as e:
        print(error)
    return(e.output.decode("utf-8"))


def git_log2(number=1, flags=['--format=%h']):
    """
    Returns the git log

    Parameters
    ----------
    number : int
    Log index

    flags : list
    List of extra flags

    Throws
    -------
    Exception if error occurs running git log
    """
    flags = ' '.join(flags)
    logging.info("Use carme save --push to push changes")
    out = bash_command("check git log", "git log " + str(number)+' '+flags)
    out = out.decode('UTF-8')
    logging.info("Local git commit value: "+out)
    return out


def git_log(number=1, flags=['--format=%h']):
    """
    Returns the git log

    Parameters
    ----------
    number : int
    Log index

    flags : list
    List of extra flags

    Throws
    -------
    Exception if error occurs running git log
    """

    number = '-' + str(number)
    flags = ' '.join(flags)
    process = Popen(['git', 'log', number, flags], stdout=subprocess.PIPE)
    out, err = process.communicate()
    out = out.decode('UTF-8')
    logging.info("Local git commit value: "+out)
    return out

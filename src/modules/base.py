"""
Variables and Functions used by multiple CLI commands
"""
import os, subprocess, logging, ruamel.yaml,  urllib.request
from subprocess import call
from os import path, pardir,getcwd
from .yamltools import *

# Global Constants
CLI_DIR     =   path.abspath(path.join(path.dirname(__file__), pardir))
BASE_DIR    =   path.dirname(CLI_DIR)
CONFIG_DIR  = 'config'
COMMANDS_DIR = 'commands'
PACKAGES_DIR = 'packages'
CONFIG_FILE= 'carme-config.yaml'
APP_DIR= 'apps'
DATA_DIR = 'data'
NOTEBOOKS_DIR = 'code/notebooks'
DOCKER_DIR= 'docker'
CWD=getcwd()

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
        result= subprocess.call(syntax, shell=True, executable='/bin/bash')
        return result
    except subprocess.CalledProcessError as e:
        print(error)
    return(e.output.decode("utf-8"))

"""
Variables and Functions used by multiple CLI commands
"""
import os

from os import path, pardir

# Global Constants
CLI_DIR     =   path.abspath(path.join(path.dirname(__file__), pardir))
BASE_DIR    =   path.dirname(CLI_DIR)
DATA_DIR    =   path.join(BASE_DIR, 'data')
DOCKER_DIR  =   path.join(DATA_DIR, 'docker')
LAUNCH_DIR  =   path.join(DATA_DIR, 'launch_files')
NOTEBOOKS_DIR=  path.join(DATA_DIR, 'notebooks')

def get_project_root():
    """
    Traverses up until it finds the folder with `carme-config.yaml` in it.
    @return: The absolute path to the project root or None if not in a project
    """
    cd = os.getcwd()
    while not os.path.exists(os.path.join(cd, "carme-config.yaml")):
        if cd == "/":
            return None
        cd = os.path.dirname(cd)
    return os.path.abspath(cd)

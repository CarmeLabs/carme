"""
Variables and Functions used by multiple CLI commands
"""

from os import path, pardir

# Global Constants
CLI_DIR     =   path.abspath(path.join(path.dirname(__file__), pardir))
BASE_DIR    =   path.dirname(CLI_DIR)
DATA_DIR    =   path.join(BASE_DIR, 'data')
DOCKER_DIR  =   path.join(DATA_DIR, 'docker')
LAUNCH_DIR  =   path.join(DATA_DIR, 'launch_files')
NOTEBOOKS_DIR=  path.join(DATA_DIR, 'notebooks')

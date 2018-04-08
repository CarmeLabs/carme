"""
Variables and Functions used by multiple CLI commands
"""
import os, subprocess, logging, ruamel.yaml

from os import path, pardir,getcwd

# Global Constants
CLI_DIR     =   path.abspath(path.join(path.dirname(__file__), pardir))
BASE_DIR    =   path.dirname(CLI_DIR)
DATA_DIR    =   path.join(BASE_DIR, 'data')
DOCKER_DIR  =   path.join(DATA_DIR, 'docker')
LAUNCH_DIR  =   path.join(DATA_DIR, 'launch_files')
NOTEBOOKS_DIR=  path.join(DATA_DIR, 'notebooks')
CWD=getcwd()


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

def setup_logger():
    """
    Sets up logging
    """
    FORMAT = 'carme: [%(levelname)s] %(message)s'
    logging.basicConfig(level=logging.INFO, format=FORMAT)


def bash_command(command, syntax):
    try:
        print("Executing "+command+":\n", syntax)
        result= subprocess.call(syntax, shell=True, executable='/bin/bash')
        return result
    except subprocess.CalledProcessError as e:
        print("error")
    return(e.output.decode("utf-8"))

def get_config(ROOT_DIR):
    kwargs=load_yaml(os.path.join(ROOT_DIR, 'carme-config.yaml'))
    return kwargs

def load_yaml(file):
    try:
        with open(file, 'r') as yaml:
            kwargs=ruamel.yaml.round_trip_load(yaml, preserve_quotes=True)
        return kwargs
    except subprocess.CalledProcessError as e:
        print("error")
    return(e.output.decode("utf-8"))

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
CONFIG_FILE= os.path.join(CONFIG_DIR, 'carme-config.yaml')
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
    logging.info("Current project root: "+os.path.abspath(cd))
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

def get_config(project_dir=get_project_root()):
    kwargs=load_yaml_file(os.path.join(project_dir, CONFIG_FILE))
    return kwargs

def update_config(kwargs, project_dir=get_project_root()):
    ruamel.yaml.round_trip_dump(kwargs, open(os.path.join(project_dir, CONFIG_FILE), 'w'))
    return kwargs

def set_config(key, value, project_dir=get_project_root()):
    kwargs=get_config(project_dir)
    kwargs[key]=value
    update_config(kwargs, project_dir)
    return kwargs

# def load_yaml_file(file):
#     try:
#         with open(file, 'r') as yaml:
#             kwargs=ruamel.yaml.round_trip_load(yaml, preserve_quotes=True)
#         return kwargs
#     except subprocess.CalledProcessError as e:
#         print("error")
#     return(e.output.decode("utf-8"))
#
# def load_yaml_url(url):
#     try:
#         response = urllib.request.urlopen(url)
#         yaml=response.read().decode('utf-8')
#         kwargs=ruamel.yaml.round_trip_load(yaml, preserve_quotes=True)
#         return kwargs
#     except subprocess.CalledProcessError as e:
#         print("Error loading", url)
#     return(e.output.decode("utf-8"))

# def append_config(carme_config,file):
#     if os.path.isfile(file):
#         print('Adding configuration to ',CONFIG_FILE,'.')
#         kwargs=load_yaml_file(file)
#         ruamel.yaml.round_trip_dump(kwargs, open(carme_config, 'a'))
#         kwargs=load_yaml_file(carme_config)
#     else:
#         print('The configuration for the application ', app, 'is not available.' )



#def update_yaml(kwargs):
#    file=os.path.join(get_project_root(),CONFIG_DIR, CONFIG_FILE)
#    ruamel.yaml.round_trip_dump(kwargs, open(file, 'w'))
#    return

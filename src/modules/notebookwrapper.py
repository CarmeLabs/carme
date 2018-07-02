'''
Carme common functions for the carme notebook and carme lab.
'''
import os
import logging
import click
from shutil import copyfile
from .base import *
from pathlib import Path

def get_image_port(image, port):
    project_root = get_project_root()
    #Decide what image to Launch
    #(2) looks for jupyter_image set in <current-project>/config/carme-config.yaml
    if project_root!=None:
        print("pr",project_root)
        config_file=os.path.join(project_root, CONFIG_DIR, CONFIG_FILE)
        kwargs=load_yaml_file(config_file)
        image, port=get_keys(image, port,kwargs)
    #(3) look for jupyter_image set in /<home>/.carme/config/carme-config.yaml
    if os.path.exists(os.path.join(str(Path.home()),'.carme',CONFIG_DIR, CONFIG_FILE)):
        kwargs=load_yaml_file(os.path.join(str(Path.home()),'.carme',CONFIG_DIR, CONFIG_FILE))
        image, port=get_keys(image, port,kwargs)
    return image,port

def get_keys(image, port, kwargs):
    if JUPYTER_IMAGE_KEY in kwargs and image is None:
        image=kwargs[JUPYTER_IMAGE_KEY]
    else:
        logging.error("Set the key "+JUPYTER_IMAGE_KEY+"in the project or /<home>/.carme/config/"+CONFIG_FILE+" to use this command.")
    if JUPYTER_PORT_KEY in kwargs and port is None:
        port=kwargs[JUPYTER_PORT_KEY]
    else:
        logging.error("Set the key "+JUPYTER_IMAGE_KEY+"in the project or /<home>/.carme/config/"+CONFIG_FILE+" to use this command.")
    return image,port

def get_flags(background):
    if background:
        flags = '-d'
    else:
        flags = '-ti --rm'
    return flags
#path=os.path.join(str(Path.home()),'.carme',CONFIG_DIR, CONFIG_FILE)

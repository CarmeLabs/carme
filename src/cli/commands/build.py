'''
Builds images.
'''

import os
import logging
from subprocess import DEVNULL, Popen
import click
from shutil import copyfile
from ...modules.base import *
from ...modules.dockerwrapper import build as build_image # renamed to avoid confict

# Set up logger
setup_logger()

@click.command()
@click.option('--force', is_flag=True, default=False, help='Force full rebuild without using cache.')
@click.option('--push', is_flag=True, default=False, help='Push image to Dockerhub (must be logged-in).')
def build(force, push):
    """
    Build project docker images.
    """
    project_root=get_project_root()

    if not os.path.exists(os.path.join(project_root, DOCKER_DIR)):
        logging.error("There are no Docker Images to build.")
        sys.exit(1)
    else:
        #Infos
        kwargs=load_yaml_file(os.path.join(project_root, CONFIG_DIR, CONFIG_FILE))

        if force:
            docop=' --no-cache '
        else:
            docop=''
        #get hash to tag dockerfile
        hash = git_log(1, ['--format=%h'])
        if hash=='':
            logging.info("No commit tag. Building with hash `init`.")
            hash='init'

        folder = os.path.join(project_root, DOCKER_DIR)
        for dir in os.listdir(folder):
            if dir+'_image' in kwargs:
                tag='carme/'+dir
            else:
                tag=kwargs[dir+'_image']

            logging.info("Building the "+tag+ "image.")
            os.chdir(os.path.join(project_root, DOCKER_DIR,dir))
            cmd='docker build '+docop+'-t '+tag+':'+'latest -t '+tag+':'+hash+'  .'
            bash_command("Building dockerfile", cmd)

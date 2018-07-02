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
@click.option('--dryrun', is_flag=True, default=False, help='Only list build command and don\'t actually build.')

def build(force, push, dryrun):
    """
    Build project docker images.
    """
    project_root=get_project_root()

    if not os.path.exists(os.path.join(project_root, DOCKER_DIR)):
        logging.error("There are no Docker Images to build.")
        sys.exit(1)
    else:
        #Infos
        if force:
            docop=' --no-cache '
        else:
            docop=''
        #get hash to tag dockerfile
        hash = git_log(1, ['--format=%h']).strip()
        if hash=='':
            logging.info("No commit tag. Building with hash `init`.")
            hash='init'

        folder = os.path.join(project_root, DOCKER_DIR)
        for dir in os.listdir(folder):
            #Loop through and only if there is a docker
            if os.path.exists(os.path.join(project_root, DOCKER_DIR, dir, 'Dockerfile')):
                print("Dockerfile check sucess",dir)
                #Image tag stored in config/<dir>.yaml or set to the dir.
                config_file=os.path.join(project_root, CONFIG_DIR, dir+'.yaml')
                if os.path.exists(config_file):
                    kwargs=load_yaml_file(config_file)

                    if dir+'-image' in kwargs:
                        tag=kwargs[dir+'-image']
                else:
                    tag='carmelabs/'+dir

                logging.info("Building the "+tag+ "image.")
                cmd='docker build '+docop+'-t '+tag+':'+'latest -t '+tag+':'+hash+'  .'

                #Now actually run the container build command.
                if dryrun==False:
                    os.chdir(os.path.join(project_root, DOCKER_DIR,dir))
                    bash_command("Building container: ", cmd)
                    if push:
                        logging.info('Pushing the '+tag+ 'image.')
                        cmd = 'docker push '+tag
                        bash_command("Pushing container: ", cmd)
                else:
                    logging.info("Build command: "+cmd)

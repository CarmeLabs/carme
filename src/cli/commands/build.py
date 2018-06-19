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
        print(kwargs)
        if force:
            docop=' --no-cache '
        else:
            docop=''

    tag = git_log(1, ['--format=%h'])
    print("returned", tag)
    if tag=='':
        logging.info("No commit tag. Building with tag `initial`.")
        tag='latest'
        cmd='docker build '+docop+'-t '+kwargs['jupyter_image']+':latest -t ' +  os.path.join(ROOT_DIR, 'docker/jupyter')
    else:
        #Build Jupyter
        cmd='docker build '+docop+'-t '+kwargs['jupyter_image']+':latest -t '+kwargs['jupyter_image']+':$(git log -1 --format=%h) ' +  os.path.join(ROOT_DIR, 'docker/jupyter')
    print (cmd)
    # bash_command("Building Jupyter", cmd)

    # TODO git commit tag
    # TODO test this to ensure functionality
    #image = build_image(nocache=force, tag=kwargs['jupyter_image']+':latest', path=os.path.join(ROOT_DIR, 'docker/jupyter'))


    #Currently there is an issue where if the build fails it will still push.
#    if push:
        #cmd='docker push '+kwargs['jupyter_image']+':latest
        # bash_command("Pushing to Dockerhub", cmd)
        #cmd='docker push '+kwargs['jupyter_image']+':$(git log -1 --format=%h)'
        #bash_command("Pushing to Dockerhub", cmd)
        #TODO test for functionality
#        image.push(dockerhub_url, tag=kwargs['jupyter_image']+':latest')

#    if jupyterhub:
        #This should update the singleuser tag
        # in /app/jupyterhub/config.yaml
#        print("tbd")

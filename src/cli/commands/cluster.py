'''
Can be used to create a manage a Kubernetes cluster.
'''

import os
import logging
import click
from shutil import copyfile
from ...modules.gitwrapper import Git
from .base import *
SUPPORTED=['gcp','azure']

setup_logger()
@click.command()
#@click.argument('cloud', default=False, help='Run Docker container in the background.')
@click.option('--dryrun', is_flag=True, default=False, help='Just the command without executing.')


def cluster(dryrun):
    """
    Can be used to create a manage a Kubernetes cluster.
    """
    ROOT_DIR=get_project_root()
    kwargs=get_config(ROOT_DIR)
    kwargs=load_yaml(CARME_CONFIG)
    if 'cluster_location' not in kwargs:
        kwargs=init_cluster(CARME_CONFIG)


def init_cluster(CARME_CONFIG):
    while True:
        cluster_location=input("Create a cluster on gcp/azure: ")  # Python 3
        if cluster_location.lower() not in SUPPORTED:
            print("I'm sorry but that is not a supported cluster.")
        else:
            break
    # @rushsteve I'm appending the config file here. How do I use your package?
    #I've setup the package data I want to merge in /data/packages/(cluster_location)
    kwargs=append_config(CARME_CONFIG,DATA_DIR+'/config_files/clusters/'+cluster_location+'.yaml')

    email= input("Please enter the email associated with your account: ")  # Python 3
    kwargs=update_config(CARME_CONFIG,'email',email)
    print(kwargs)
    #config['email']= input("Please enter the email associated with your account: ")  # Python 3
    #Create the launch_file in the user directory
    #ruamel.yaml.round_trip_dump(config, open(self.launch_file, 'w'))
    #copyfile(self.notebooks_dir+'/clusters/'+cluster_location+'.ipynb', self.cwd+'/'+cluster_location+'.ipynb')
    #copyfile(self.base_dir+'/data/readme.md', self.cwd+'/readme.md')

    #if self.options['--jupyter']:
    #      print("Appending Jupyter")
    #    self.append_launch_file('jupyter')

    return kwargs

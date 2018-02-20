"""Wrapper for the Docker SDK providing some basic utilities. Anything more complex should call the SDK itself."""
import docker
import os
from ruamel.yaml import YAML
from tempfile import NamedTemporaryFile
from subprocess import call
from yamltools import folder_merge_yaml
import logging

# Setup docker client
client = docker.from_env()

# Set up logger
FORMAT = 'carme: [%(levelname)s] %(message)s'
logging.basicConfig(level=logging.INFO, format=FORMAT)

def permcheck(func):
    """Decorator to check if Docker is installed, and if the user has permissions for it."""
    def inner():
        path = os.getenv('PATH')
        # This only iterates through the locations in the PATH so it is pretty cheap
        for p in path.split(os.path.pathsep):
            p = os.path.join(p, "docker")
            if os.path.exists(p):
                if os.access(p, os.X_OK):
                    func()
                else:
                    logging.error("You do not have permisison to manage Docker")
                    raise PermissionError
            else:
                loggint.error("Docker binary not found on PATH")
                raise FileNotFoundError
    return inner

def check(func);
    """Decorator to check if Docker is in swarm mode, and also calls permcheck()"""
    @permcheck
    def inner():
        if client.info()['Swarm'] is not "inactive":
            func()
        else:
            # It might be a good idea to just call init() here but for debug purposes I left it as an error
            logging.warning("Docker not in swarm mode. Would you like to enable swarm mode? (y/n) [n]")
            answer = input().lower()
            if answer == 'y' or answer == 'yes':
                swarm_init()
    return inner

@check
def carme_start(path: str):
    """
    Starts a Docker stack named 'carme' from the compositor compose file of fo the the current project.
    Generally this should be the only function called from this file unless you are doing something more complicated. 

    @param path: path to the project's compose file 
    @return: boolean value of success status
    """
    if not os.path.exists(path) or os.path.isdir(path):
        return False

    file = folder_merge_yaml(path)
    
@check
def carme_stop():
    return stack_remove("carme")

@permcheck
def swarm_init():
    """
    Equivalent to 'swarm init'

    @return: boolean value of success status
    """
    try:
        client.swarm.init(name="carme")
        return True
    except Exception as err:
        loggint.error(err)
        return False

@check
def service_info(service_id: str):
    """
    Get information about a service

    @param service_id: the ID of the service you want info on
    @return: a Service object representing the service
    """
    return client.service.get(service_id)

@check
def service_list():
    """
    List all the services

    @return: a List of Service objects    
    """
    return client.service.list()

@check
def service_remove(service_id: str):
    """
    Stops and removes a service. This can also be done with Service.remove().

    @param service_id: the ID of the service you want to remove.
    @return: boolean value of success status
    """

    try:
        client.service.get(service_id).remove()
        return True
    except Exception as err:
        logging.error(err)
        return False
@check
def stack_start(name: str, compose_file: str):
    """Deploys a stack. Due to limitations of the Docker SDK this calls the actual Docker CLI."""
    proc = call(["docker", "stack", "deploy", "-f", compose_file, name])
    if proc.returncode is not 0:
        logging.error("`docker stack deploy` exited with non-zero exit code.")
        return False
    return True
    
def stack_remove(name: str):
    """Removes a stack. Due to limitations of the Docker SDK this calls the actual Docker CLI."""
    proc = call(["docker", "stack", "rm", name])
    if proc.returncode is not 0:
        logging.error("`docker stack remove` exited with non-zero exit code.")
        return False
    return True

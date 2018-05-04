"""Wrapper for the Docker SDK providing some basic utilities. Anything more complex should call the SDK itself."""
import docker
import os
from ruamel.yaml import YAML
from tempfile import NamedTemporaryFile
from subprocess import call
from .yamltools import * #had trouble inmporting
import logging
import stat

# Setup docker client
client = docker.from_env()

# Set up logger
FORMAT = 'carme: [%(levelname)s] %(message)s'
logging.basicConfig(level=logging.INFO, format=FORMAT)

# FIXED
def permcheck(func):
    """Decorator to check if Docker is installed, and if the user has permissions for it."""
    def inner():
        path = os.getenv('PATH')
        # This only iterates through the locations in the PATH so it is pretty cheap
        bin_found = False
        while not bin_found:
            for p in path.split(os.path.pathsep):
                bin_path = os.path.join(p, "docker")
                if os.path.exists(bin_path):
                    bin_found = True
                    if os.access(bin_path, os.X_OK):
                        func()
                    else:
                        logging.error("You do not have permisison to manage Docker")
                        raise PermissionError
                    break
        if not bin_found:
            logging.error("Docker binary not found on PATH")
            raise FileNotFoundError
        # TODO: Change to more than just this default path?
        socket_path = "/var/run/docker.sock"
        if not os.path.exists(socket_path):
            logging.error("Docker daemon not found, try starting the Docker service")
            raise FileNotFoundError
        docker_mode = os.stat(socket_path).st_mode
        isSocket = stat.S_ISSOCK(docker_mode)
        if not isSocket:
            logging.error("Docker daemon is currently not running, try starting the Docker service")
            raise EnvironmentError
    return inner

# TODO: Debug this function, ensure functionality
def check(func):
    """Decorator to check if Docker is in swarm mode, and also calls permcheck()"""
    @permcheck
    def inner():
        try:
            if client.info()['Swarm'] is not "inactive":
                func()
            else:
                # It might be a good idea to just call init() here but for debug purposes I left it as an error
                logging.warning("Docker not in swarm mode. Would you like to enable swarm mode? (y/n) [n]")
                answer = input().lower()
                if answer == 'y' or answer == 'yes':
                    swarm_init()
        except Exception:
            raise Exception
    return inner

# TODO: Debug this function, ensure functionality
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

    outfile = folder_merge_yaml(path)
    stack_start("carme", outfile)

# TODO: Debug this function, ensure functionality
@check
def build(**kwargs):
    """
    Just wraps the docker SDK's build function.

    @return an Image object
    """
    return client.images.build(**kwargs)

# TODO: Debug this function, ensure functionality
@check
def carme_stop():
    return stack_remove("carme")

# TODO: Debug this function, ensure functionality
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
        logging.error(err)
        return False

# TODO: Debug this function, ensure functionality

@check
def service_info(service_id: str):
    """
    Get information about a service

    @param service_id: the ID of the service you want info on
    @return: a Service object representing the service
    """
    return client.service.get(service_id)

# TODO: Debug this function, ensure functionality
@check
def service_list():
    """
    List all the services

    @return: a List of Service objects
    """
    return client.service.list()

@check
def service_create(image: str, **kwargs):
    """
    Starts a service. This can also be done with Service.start()

    @param image: the name of the image you want to create a service for
    @return: a Service object representing the service
    """

    return client.service.create(image, command=kwargs['command'], **kwargs)

# TODO: Debug this function, ensure functionality
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

# TODO: Debug this function, ensure functionality
@check
def stack_start(name: str, compose_file: str):
    """Deploys a stack. Due to limitations of the Docker SDK this calls the actual Docker CLI."""
    proc = call(["docker", "stack", "deploy", "-f", compose_file, name])
    if proc.returncode is not 0:
        logging.error("`docker stack deploy` exited with non-zero exit code.")
        return False
    return True

# TODO: Debug this function, ensure functionality
def stack_remove(name: str):
    """Removes a stack. Due to limitations of the Docker SDK this calls the actual Docker CLI."""
    proc = call(["docker", "stack", "rm", name])
    if proc.returncode is not 0:
        logging.error("`docker stack remove` exited with non-zero exit code.")
        return False
    return True

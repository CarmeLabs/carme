import logging
import sys
import click
from shutil import copyfile
from .base import *
import ruamel.yaml
from string import Formatter

class CommandFormatter(Formatter):
    """This will replace the values in the template with values from the kwargs.
    """
    def get_value(self, key, args, kwds):
        if isinstance(key, str):
            try:
                return kwds[key]
            except KeyError:
                return key
        else:
            return Formatter.get_value(key, args, **kwds)

def get_project_commands():
    """
    Gets the list of commands from the commands directory.
    @return: A commented list of the commands
    """
    ROOT_DIR=get_project_root()
    CARME_COMMANDS=os.path.join(ROOT_DIR, 'commands','carme-commands.yaml')
    if os.path.isfile(CARME_COMMANDS):
        commands=load_yaml_file(CARME_COMMANDS)
    else:
        print("No commands file found.")
        exit()
    return commands

def sub_keys(template, kwargs):
    fmt = CommandFormatter()
    command= fmt.format(template, **kwargs)
    return command

def execute(command, commands, package, kwargs, docker=False, dryrun=False):
    logging.info("Running the command: "+ command)
    logging.info("Template: "+ commands[command])
    syntax=sub_keys(commands[command], kwargs)
    if docker==True:
        syntax= 'docker exec -ti ' +kwargs[package+'_image']+' sh -c "'+syntax+'"'
    logging.info("Values: "+ syntax)
    if not dryrun:
        bash_command(command, syntax)

#

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
                val=kwds[key]
                if val != None:
                    return kwds[key]
                else:
                    logging.error("Value for key="+ key+ \
                    " is not set in the /config/<command>.yaml file. Please set the key and rerun the command." )
                    exit()
            except KeyError:
                logging.error("The Key="+ key+ \
                " is not set in the /config/<command>.yaml file. Please set the key and rerun the command." )
                exit()
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

def execute(command, commands, package, project_root, kwargs, docker=False, dryrun=False, server =False):
    logging.info("Running the command: "+ command)
    logging.info("Template: "+ commands[command])
    project_name = os.path.basename(project_root)
    #slighty different if it is a script
    if commands[command][-3:]=='.sh'or commands[command][0:7]=='script:':
        commands[command]=commands[command].replace('script:', '')
        script_path=os.path.join(project_root, 'commands', 'scripts',commands[command])
        if remote ==false:
            syntax= 'bash -x '+script_path
        else:
            syntax='ssh {server_name}@{ip_address} bash -s > '+script_path
    syntax=sub_keys(commands[command], kwargs)
    #slightly different if it is docker.
    if docker==True:
        syntax= 'docker run -it -v '+project_root+':/home/'+project_name+' '+kwargs[package+'_image']+' sh -c "'+syntax+'"'

    if dryrun:
        logging.info("Values: "+ syntax)
    else:
        bash_command(command, syntax)

#

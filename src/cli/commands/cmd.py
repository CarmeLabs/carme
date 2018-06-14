'''
Run a command from templates in the command directory.
'''

import os
import logging
import sys
import click
from shutil import copyfile
from ...modules.base import *
from ...modules.commandswrapper import *
from ...modules.yamltools import *
import ruamel.yaml

#set up logger
setup_logger()
@click.command()
#@click.argument('command', callback=validate_command, default='list')
@click.argument('package')
@click.argument('command')
@click.option('--dryrun', is_flag=True, default=False, help='Only print the command, do not run.')

def cmd(package, command, dryrun):
    """Runs commands from the commands folder."""
    #Finds the project root directory.
    project_dir=get_project_root()
    #Loads the configuration in the root directory.
    package_file=package+'.yaml'
    kwargs=load_yaml_file(os.path.join(project_dir, CONFIG_DIR, package_file))

    #Loads the commands available in the commands directory.
    commands=load_yaml_file(os.path.join(project_dir, COMMANDS_DIR, package_file))
    #The list command is used to show availabe commands.
    if command=='list':
        logging.info('These commands are currently installed:')
        ruamel.yaml.dump(commands, sys.stdout, Dumper=ruamel.yaml.RoundTripDumper)
    #This check to see if there are a series of commands passed as a list (example: [com1, com2, com3]).
    elif isinstance(commands[command], ruamel.yaml.comments.CommentedSeq):
        logging.info('Executing command block '+command+ ':')
        for x in commands[command]:
            execute(x, commands, kwargs, dryrun)
    #This attempts to execute a single command.
    else:
        execute(command, commands, kwargs, dryrun)

def validate_command(ctx, param, value):
    """Validates that the desired command is in the commands file.
    """
    commands=get_project_commands()
    if value !='list' and value not in commands:
        raise logging.warning('This is not a valid command. Use *list* to show installed commands.')
    return value

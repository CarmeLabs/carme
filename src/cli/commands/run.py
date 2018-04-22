'''
Run a command from templates in the command directory.
'''

import os
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
            return Formatter.get_value(key, args, kwds)

def sub_keys(template, kwargs):
    fmt = CommandFormatter()
    command= fmt.format(template, **kwargs)
    return command

def validate_command(ctx, param, value):
    """Validates that the desired command is in the commands file.
    """
    commands=get_project_commands()
    if value !='list' and value not in commands:
        raise logging.warning('This is not a valid command. Use *list* to show installed commands.')
    return value

def execute(command, commands, kwargs, dryrun=False):
    logging.info("Running the command: "+ command)
    logging.info("Template: "+ commands[command])
    syntax=sub_keys(commands[command], kwargs)
    logging.info("Values: "+ syntax)
    if not dryrun:
        bash_command(command, syntax)

# Set up logger
setup_logger()

@click.command()
@click.argument('command', callback=validate_command, default='list')
@click.option('--dryrun', is_flag=True, default=False, help='Only print the command, do not run.')
def run(command, dryrun):
    """Runs commands from the commands folder."""
    #Finds the project root directory.
    ROOT_DIR=get_project_root()
    #Loads the configuration in the root directory.
    kwargs=get_config(ROOT_DIR)
    #Loads the commands available in the commands directory.
    commands=get_project_commands()
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

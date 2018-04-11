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
    def get_value(self, key, args, kwds):
        if isinstance(key, str):
            try:
                return kwds[key]
            except KeyError:
                return key
        else:
            return Formatter.get_value(key, args, kwds)

def validate_command(ctx, param, value):
    commands=get_project_commands()
    if value !='list' and value not in commands:
        raise click.BadParameter('This is not a valid command. Use *list* to show installed commands.')
    return value

def sub_keys(template, kwargs):
    fmt = CommandFormatter()
    command= fmt.format(template, **kwargs)
    return command

# Set up logger
setup_logger()

@click.command()
@click.argument('command', callback=validate_command, default='list')
@click.option('--dryrun', is_flag=True, default=False, help='Only print the command, do not run.')
def run(command, dryrun):
    """Runs commands from the commands folder."""
    ROOT_DIR=get_project_root()
    kwargs=get_config(ROOT_DIR)
    commands=get_project_commands()
    if command=='list':
        ruamel.yaml.dump(commands, sys.stdout, Dumper=ruamel.yaml.RoundTripDumper)
    else:
        print ("Running the command: ", command)
        click.echo("Template: "+ commands[command])
        syntax=sub_keys(commands[command], kwargs)
        print(syntax)
        if not dryrun:
            bash_command(command, syntax)

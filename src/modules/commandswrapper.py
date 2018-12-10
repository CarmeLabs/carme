import logging
import sys
import click
import os
from shutil import copyfile
from .base import get_project_root, load_yaml_file, bash_command
import ruamel.yaml
from string import Formatter


class CommandFormatter(Formatter):
    """This will replace the values in the template with values from the kwargs.
    """

    def get_value(self, key, args, kwds):
        if isinstance(key, str):
            try:
                val = kwds[key]
                if val != None:
                    return kwds[key]
                else:
                    logging.error("Value for key=" + key +
                                  " is not set in the /config/<command>.yaml file. Please set the key and rerun the command.")
                    exit()
            except KeyError:
                logging.error("The Key=" + key +
                              " is not set in the /config/<command>.yaml file. Please set the key and rerun the command.")
                exit()
        else:
            return Formatter.get_value(key, args, **kwds)


def get_project_commands():
    """
    Gets the list of commands from the commands directory.
    @return: A commented list of the commands
    """
    ROOT_DIR = get_project_root()
    CARME_COMMANDS = os.path.join(ROOT_DIR, 'commands', 'carme-commands.yaml')
    if os.path.isfile(CARME_COMMANDS):
        commands = load_yaml_file(CARME_COMMANDS)
    else:
        print("No commands file found.")
        exit()
    return commands


def sub_keys(template, kwargs):
    fmt = CommandFormatter()
    command = fmt.format(template, **kwargs)
    return command


def execute(command, commands, package, project_root, kwargs, docker=False, dryrun=False, yes=False):
    logging.info("Running the command: " + command)
    logging.info("Template: " + commands[command])
    project_name = os.path.basename(project_root)
    # slighty different if it is a script
    if commands[command][0:7] == 'script':
        commands[command] = commands[command].replace('script:', '')
        script_path = os.path.join('./commands', 'scripts', command+'.sh')
        # to be implemented later. Ability to execute remotely.
        remote = False
        if remote == False:
            syntax = 'source '+script_path

        else:
            syntax = 'ssh {server_name}@{ip_address} bash -s > '+script_path
    else:
        # This will update.
        syntax = sub_keys(commands[command], kwargs)
    # slightly different if it is docker.
    if docker == True:
        syntax = 'docker run -it -v '+project_root+':/home/' + \
            project_name+' '+kwargs[package+'_image']+' sh -c "'+syntax+'"'

    logging.info("Command: " + syntax)

    # As a security protection, confirm they really want to execute the command.  No confirmation needed for dry run. s
    if not yes and not dryrun:
        cont = input(
            "Press 'y' to execute the above command, 's' to skip, enter to quit. ")
        if cont == 'y':
            bash_command(command, syntax)
        elif cont == 's':
            logging.info("Skipping the above command")
        else:
            logging.info("Quitting")
            quit()
    elif not dryrun:
        bash_command(command, syntax)

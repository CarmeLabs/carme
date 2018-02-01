"""
carme

Usage:
  carme -h | --help
  carme -v | --version
  carme hello
  carme init (azure|gcp) [--jupyter][--airflow][--force]
  carme add_config <app>
  carme app <app> <command> [--dry-run]
  carme cluster <command> [--dry-run]
  carme save [--message]

Options:
  -h --help                         Show this screen.
  -v --version                      Show version.
  -f --force                        Force.
  --jupyter                         Set config to include jupyter.
  --echo                            Only print the comand, don't execute.

Examples:
  carme cluster new

Help:
  For help using this tool, please see the Github repository:
  https://github.com/carme/carme
"""

from inspect import getmembers, isclass
from docopt import docopt
from . import __version__ as VERSION
from os.path import abspath, dirname, join, isfile
import os
from subprocess import PIPE, Popen as popen
from unittest import TestCase
from carme import __version__ as VERSION

def main():
    """Main CLI entrypoint."""
    import carme.commands
    options = docopt(__doc__, version=VERSION)

    # Here we'll try to dynamically match the command the user is trying to run
    # with a pre-defined command class we've already created.
    for (k, v) in options.items():
        if hasattr(carme.commands, k) and v:
            module = getattr(carme.commands, k)
            carme.commands = getmembers(module, isclass)
            command = [command[1] for command in carme.commands if command[0] != 'Base'][0]
            command = command(options)
            command.run()

# def runit(command):
#     print(command)
#     input=command.split()
#     if input[0]!="carme":
#         input.insert(0,"carme")
#     return popen(input, stdout=PIPE).communicate()[0]
#
# def main():
#     """Main CLI entrypoint."""
#     #print(__doc__)
#     options = docopt(__doc__, version=VERSION)
#     cli(options)
#
# def cli(options):
#     import carme.commands as kc
#     """Main CLI entrypoint."""
#     # Here we'll try to dynamically match the command the user is trying to run
#     # with a pre-defined command class we've already created.
#     for (k, v) in options.items():
#           if hasattr(kc, k) and v:
#             module = getattr(kc, k)
#             kc = getmembers(module, isclass)
#             print("kc",kc)
#             command = [command[1] for command in kc if command[0] != 'Base'][0]
#             print("command",command)
#             command = command(options)
#             print("command2",command)
#             command.run()

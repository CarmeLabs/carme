'''
Generates fake data from two files
'''
import os
import logging
import click
from shutil import copyfile, copytree
from .package import _install_package
from ...modules.packager import Packager
from ...modules.base import *
from ...modules.yamltools import *
from .git import _git
from ...modules.generationtools.synthesize import synthesize_table

@click.command()
@click.argument('input_file', nargs=1)
@click.argument('output_file', nargs=1)
def generate(input_file, output_file):
    """
    Takes an input file copies the data, then generates 
    fake data to the output file
    """
    synthesize_table(input_file,output_file)
    

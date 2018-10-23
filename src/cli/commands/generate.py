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

@click.command()
@click.argument('input_file', nargs=1)
@click.argument('output_file', nargs=1)
def generate(input_file, output_file):
    """
    Takes an input file copies the data, then generates 
    fake data to the output file
    """
    data = []
    with open(input_file, 'r') as f:
        for line in f:
            temp = line.split()
            data.append(temp)


    hash_data(data) #temp function that will actually generate the fake data from the real data"
    pass

    
    with open(output_file,'w') as o:
        for line in data:
            for word in line:
                o.write(word)
                o.write(' ')
            o.write('\n')


def hash_data(data):
    pass
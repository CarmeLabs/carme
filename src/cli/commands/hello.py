"""The hello command."""

import click
from json import dumps

@click.command()
def hello():
    print('Hello, world! version 2')

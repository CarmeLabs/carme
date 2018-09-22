'''
Delete and remove all images locally to free up disk space.
'''
import click
from ...modules.base import bash_command, setup_logger
# Set up logger
setup_logger()
@click.command()
def cleanup():
    """
    Delete and remove all images.
    """
    cmd = 'docker rmi --force  $(docker images -a -q)'
    bash_command("Deleting all images", cmd)

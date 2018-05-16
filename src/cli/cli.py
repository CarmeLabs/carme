import click
from .commands import new, save, package, connect, lab, build, notebook, cmd
#from .commands.packages import samppack

#create a sample list of packages. Could pull from config.
packages=['samppack']

@click.group()
@click.version_option()
def carme():
    pass

@carme.command('hello')
def hello():
    """
    Prints a simple hello world message.
    """
    print('Hello, world! version 3')

# commands from external files ie the commands folder must be manually
# imported then added to the group.
carme.add_command(lab)
carme.add_command(new)
carme.add_command(save)
carme.add_command(package)
carme.add_command(connect)
carme.add_command(build)
carme.add_command(notebook)
#carme.add_command(cluster)
carme.add_command(cmd)

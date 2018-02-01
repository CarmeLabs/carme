"""The app command."""

from json import dumps
import ruamel.yaml
import os
import sys
from .base import Base
from .clusters.azure import *
from .clusters.gcp import *


class Cluster(Base):
    """Cluster commands"""
    def run(self):
        self.check_launch_file()
        if self.launch_config['cluster_location']=='azure':
            print('Azure Cloud')
            self.cluster_commands=azure_commands(self)
        elif self.launch_config['cluster_location']=='gcp':
            #print('Google cloud')
            self.cluster_commands=gcp_commands(self)
        if self.options['<command>']=='list':
            print("Listing out available commands.")
            print(ruamel.yaml.dump(self.cluster_commands, sys.stdout, Dumper=ruamel.yaml.RoundTripDumper))
        elif self.options['<command>']=='login':
            print("Logging in.")
            result=self.bash_command('login',self.cluster_commands['login'])
            print(result)
            print(type(result))
            #print(self.launch_config)
        elif self.options['<command>'] in self.cluster_commands:
            print(self.bash_command(self.options['<command>'],self.cluster_commands[self.options['<command>']]))

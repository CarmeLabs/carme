'''
Creates a new cluster.
'''
from json import dumps
import ruamel.yaml
from shutil import copyfile
import os
import sys
from .base import Base
from .clusters.azure import *
from .clusters.gcp import *
supported_clusters=['gcp','azure']


class Cluster(Base):
    """Cluster commands"""
    def run(self):
        #print("the following keys are required", requiredKeys)
        if self.check_launch_file():
            if not self.check_key("cluster_location"):
                #This performs the initial configuration if key isn't there
                print("Updating launchfile to include cluster information.")
                self.cluster_location = input("Please enter cloud provider ("+'/'.join(supported_clusters)+"):")
                if(self.cluster_location in supported_clusters):
                    config=self.load_yaml(self.launch_dir+'/clusters/'+self.cluster_location+'.yaml')
                else:
                    logging.error("Only "+'/'.join(supported_clusters)+"are currently supported")
                config['email']= input("Please enter the email associated with your account: ")  # Python 3
                #Create the launch_file in the user directory
                copyfile(self.notebooks_dir+'/clusters/'+self.cluster_location+'.ipynb', self.cwd+'/'+self.cluster_location+'.ipynb')
                self.append_launch_file(config)
                self.options['<command>']='list'


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


        #cluster_location="gcp"
        #config=self.load_yaml(self.launch_dir+'/clusters/'+cluster_location+'.yaml')
        #print(config)
        #if self.check_keys()
        # if self.launch_config['cluster_location']=='azure':
        #     print('Azure Cloud')
        #     self.cluster_commands=azure_commands(self)
        # elif self.launch_config['cluster_location']=='gcp':
        #     #print('Google cloud')
        #     self.cluster_commands=gcp_commands(self)
        # if self.options['<command>']=='list':
        #     print("Listing out available commands.")
        #     print(ruamel.yaml.dump(self.cluster_commands, sys.stdout, Dumper=ruamel.yaml.RoundTripDumper))
        # elif self.options['<command>']=='login':
        #     print("Logging in.")
        #     result=self.bash_command('login',self.cluster_commands['login'])
        #     print(result)
        #     print(type(result))
        #     #print(self.launch_config)
        # elif self.options['<command>'] in self.cluster_commands:
        #     print(self.bash_command(self.options['<command>'],self.cluster_commands[self.options['<command>']]))

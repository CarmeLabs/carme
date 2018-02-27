"""The base command."""
import os
from shutil import copyfile
import ruamel.yaml
import subprocess
from shutil import copyfile
import logging

class Base(object):
    """A base command."""

    def __init__(self, options, *args, **kwargs):
        self.options = options
        self.args = args
        self.cli_dir=os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
        self.base_dir=os.path.dirname(self.cli_dir)
        self.data_dir=self.base_dir+'/data'
        self.docker_dir=self.data_dir+'/docker'
        self.launch_dir=self.data_dir+'/launch_files'
        self.notebooks_dir=self.data_dir+'/notebooks'
        self.cwd=os.getcwd()
        self.launch_file = self.cwd+'/config.yaml'
        self.launch_config = {}
        self.cluster_commands = {}
        self.app_commands = {}
        FORMAT = 'carme: [%(levelname)s] %(message)s'
        logging.basicConfig(level=logging.INFO, format=FORMAT)

    def message(self, mess):
            print('Adding configuration for '+mess+' to launch.yaml.')

    def append_launch_file(self, config):
        if os.path.isfile(self.launch_file):
            ruamel.yaml.round_trip_dump(config, open(self.launch_file, 'a'))
            self.launch_config=self.load_yaml(self.launch_file)
        return True

    def bash_command(self, command, syntax):
        if self.options['--dry-run']:
            print("Printing (not running) "+command+":\n", syntax)
        else:
            try:
                print("Executing "+command+":\n", syntax)
                result= subprocess.call(syntax, shell=True, executable='/bin/bash')
                return result
            except subprocess.CalledProcessError as e:
                return(e.output.decode("utf-8"))

    def check_launch_file(self):
        if os.path.exists(self.launch_file):
            self.launch_config=self.load_yaml(self.launch_file)
            return True
        else:
            print("The launch.yaml file is not present in curently directory.  Run 'carme new <projectname>' to create it.")
            quit()

    def check_keys(self, requiredKeys=None):
        if os.path.exists(self.launch_file):
            self.launch_config=self.load_yaml(self.launch_file)
            for key in requiredKeys:
                if key !=None and key not in self.launch_config:
                    quit()
        else:
            print("The launch.yaml file is not present in curently directory.  Run 'carme new <projectname>' to create it.")
            quit()

    def check_key(self, key):
            self.launch_config=self.load_yaml(self.launch_file)
            if key not in self.launch_config:
                 return False
            else:
                return True

    def check_overwrite_launch_file(self):
        if os.path.isfile(self.launch_file) and not self.options['--force']:
            print('The launch.yaml file already exists in the current directory. Add the --force flag to overwrite.' )
            quit()
        else:
            return True

    def load_yaml(self, file):
        with open(file, 'r') as yaml:
            kwargs=ruamel.yaml.round_trip_load(yaml, preserve_quotes=True)
        return kwargs

    def run(self):
        raise NotImplementedError('You must implement the run() method yourself!')

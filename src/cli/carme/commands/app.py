"""The app command."""


from json import dumps
import os
from .base import Base
import ruamel.yaml
import sys
from .apps.jupyter import *

class App(Base):
    """Cluster commands"""
    def run(self):
        self.check_launch_file()
        app_file=self.launch_dir+'/apps/'+self.options['<app>']+'.yaml'
        if os.path.isfile(app_file):
            if self.options['<app>']=='jupyter':
                jupyter_action(self)
            else:
                print("The application "+self.options['<app>']+"is not available yet. Use `carme -h` to see available apps.")

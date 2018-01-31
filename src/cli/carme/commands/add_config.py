"""The app command."""


from json import dumps
from .base import Base
import ruamel.yaml

class Add_config(Base):
    """Cluster commands"""
    def run(self):
        self.append_launch_file(self.options['<app>'])

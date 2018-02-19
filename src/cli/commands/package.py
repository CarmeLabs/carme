"""
Manage project packages
"""

from .base import Base
from .modules.packager import Packager
import logging

# Set up logger
FORMAT = 'carme: [%(levelname)s] %(message)s'
logging.basicConfig(level=logging.INFO, format=FORMAT)

class Package(Base):
    def install(self, package_path, project_dir):
        logging.info("Installing package from: " + package_path)
        Packager(package_path, project_dir).install()
        
    def remove(self, package_path, project_dir):
        Packager(package_path, project_dir).install()

    def download(self, package_path, project_dir):
        Packager(package_path, project_dir).install()

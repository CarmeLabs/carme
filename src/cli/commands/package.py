"""
Manage project packages
"""

from .base import Base

class Package(Base):
    def run(self):
        print("Creating new project folder.")

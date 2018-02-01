"""
Creates a new project
"""

from .base import Base

class New(Base):
    def run(self):
        print("Creating new project folder.")
        print(self.options)

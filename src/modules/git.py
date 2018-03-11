'''
Carme git commands
'''

from .base import Base
import sys
import os
import logging
import subprocess


# Set up logger
FORMAT = 'carme: [%(levelname)s] %(message)s'
logging.basicConfig(level=logging.INFO, format=FORMAT)

class Git():
    def init(self, project_dir):
        # Run git initial functions if possible
        try:
            subprocess.Popen(["git", "init"], cwd=project_dir)
        except Exception as err:
            logging.error("Error when running 'git init'")
            raise err

    def commit(self, message, project_dir):
        if message:
            self.message = message
        else:
            logging.info("No message provided. Defaulting to 'Update'")
            self.message = "Update"
        try:
            subprocess.Popen(["git", "commit", "-m", self.message], cwd=project_dir)
        except Exception as err:
            logging.error("Error when running 'git commit'")
            raise err
    
    def add(self, files, project_dir):
        if(len(files) == 0):
            try:
                subprocess.Popen(["git", "add", "."], cwd=project_dir)
            except Exception as err:
                logging.error("Error when running 'git add'")
                raise err
        else:
            for i in range(len(files)):
                try:
                    subprocess.Popen(["git", "add", files[i]], cwd=project_dir)
                except Exception as err:
                    logging.error("Error when running 'git add'")
                    raise err

    def remote_add(self, project_dir, repo_url):
        try:
            subprocess.Popen(["git", "remote", "add", "origin", repo_url], cwd=project_dir)
        except Exception as err:
            logging.error("Error when running 'git remote'")
            raise err

    def push(self, project_dir):
        try:
            subprocess.Popen(["git", "push", "-u", "origin", "master"], cwd=project_dir)
        except Exception as err:
            logging.error("Error when running 'git push'")
            raise err

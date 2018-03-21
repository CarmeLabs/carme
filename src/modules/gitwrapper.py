'''
Carme git commands
'''

import os
import logging
import subprocess
import getpass
from subprocess import DEVNULL, Popen


# Set up logger
FORMAT = 'carme: [%(levelname)s] %(message)s'
logging.basicConfig(level=logging.INFO, format=FORMAT)

class Git():
    """
    A git wrapper that calls git commands directly from the shell

    Commands supported: git init, git add, git commit, git push, git remote add
    """

    @staticmethod
    def init(project_dir):
        """
        Initializes a git repository

        Parameters
        ----------
        project_dir : string
        Working directory of the new carme project

        Throws
        -------
        ValueError if project_dir isn't valid
        Exception if error occurs when running `git init`
        """

        if project_dir == "" or not os.path.exists(project_dir):
            raise ValueError("Invalid directory")
        try:
            Popen(["git", "init"], cwd=project_dir, stdout=DEVNULL)
        except subprocess.CalledProcessError:
            raise Exception("Error when running git init")

    @staticmethod
    def commit(message, project_dir):
        """
        Commits the indexed files

        Parameters
        ----------
        project_dir : string
        Working directory of the new carme project

        message : string
        Message of the commit

        Throws
        -------
        ValueError if project_dir isn't valid
        Exception if error occurs when running `git commit`
        """

        if project_dir == "" or not os.path.exists(project_dir):
            raise ValueError("Invalid directory")
        try:
            Popen(["git", "commit", "-m", message], cwd=project_dir, stdout=DEVNULL)
        except subprocess.CalledProcessError:
            raise Exception("Error when running git commit")

    @staticmethod
    def add(project_dir):
        """
        Indexes all of the project files

        Parameters
        ----------
        project_dir : string
        Working directory of the new carme project

        Throws
        -------
        ValueError if project_dir isn't valid
        Exception if error occurs when running `git add`
        """
        
        if project_dir == "" or not os.path.exists(project_dir):
            raise ValueError("Invalid directory")
        try:
            Popen(["git", "add", "."], cwd=project_dir, stdout=DEVNULL)
        except subprocess.CalledProcessError:
            raise Exception("Error when running git add")

    @staticmethod
    def remote_add(project_dir, repo_url):
        """
        Connects to a remote git repository

        Parameters
        ----------
        project_dir : string
        Working directory of the new carme project

        repo_url : string
        URL of the remote repository

        Throws
        -------
        ValueError if project_dir isn't valid
        Exception if error occurs when running `git remote add`
        """

        if project_dir == "" or not os.path.exists(project_dir):
            raise ValueError("Invalid directory")
        try:
            Popen(["git", "remote", "add", "origin", repo_url], \
            cwd=project_dir, stdout=DEVNULL)
        except subprocess.CalledProcessError:
            raise Exception("Error when running git remote add")

    @staticmethod
    def push(project_dir):
        """
        Pushes all of the staged files to the remote repository

        Parameters
        ----------
        project_dir : string
        Working directory of the new carme project

        Throws
        -------
        ValueError if project_dir isn't valid
        ValueError if the git URL is invalid
        Exception if error occurs when running `git remote add`
        """

        if project_dir == "" or not os.path.exists(project_dir):
            raise ValueError("Invalid directory")
        try:
            process = Popen(['git', 'config', '--get', 'remote.origin.url'], \
            stdout=subprocess.PIPE)
            out, err = process.communicate()
            # Validate before parsing
            if not str(out):
                raise ValueError("Git URL not set, run `carme connect` to set URL")
            if str(out).find("https://") == -1:
                raise ValueError("Git URL not valid, ensure the validation of the URL set")
            # Parse the URI
            url = str(out).split("https://")[1]
            url = url[0:url.find(".git")+4]
            user = input('Username: ')
            password = getpass.getpass('Pasword: ')
            uri = ("https://"+user+":"+password+"@"+url).strip()
            Popen(["git", "push", "-u", uri], cwd=project_dir, stdout=DEVNULL)
        except subprocess.CalledProcessError:
            raise Exception("Error when running git push")

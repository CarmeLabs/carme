"""
Module for managing packages. Provides facilites for installing, removing and updating.
"""

import os, sys
import validators
import mimetypes
import logging
from urllib import retrieve
from zipfile import ZipFile
from shutil import copyfile
from tempfile import mkdtemp

# A constant for the downloaded package cache
PKG_CACHE = os.path.join(os.path.dirname(sys.modules['__main__'].__file__), 'cache/')

# Set up logger
FORMAT = 'carme: [%(levelname)s] %(message)s'
logging.basicConfig(level=logging.INFO, format=FORMAT)

class Package:
    """
    Object for managing a package
    """
    project_path: str = None
    zip_path: str = None
    unzipped_path: str = None
    download_URL: str = None

    def __init__(self, package_path: str, project_path: str):
        """
        Creates a new instance of the package object.

        @param package_path: The local path or URL to the package to be installed. Can be to either a folder or a zip archive.
        @param project_path: The local path to the project that the package is going to be installed into.
        """
        absp = os.path.abspath(package_path)
        # If package_path was a valid URL then download it
        if validators.url.url(package_path):
            self.download_URL = package_path

        # If the absoulte path of package_path exists as a...
        elif os.path.exists(absp):
            # folder
            if os.path.isdir(absp):
                self.unzipped_path = absp

            # Zip file
            elif os.path.isfile(absp) && mimetypes.guess_type(absp) == "application/zip":
                self.zip_path = absp

        # Otherwise it was an error and log it
        else:
            logging.error("Invalid file path or URL: " + package_path)
            raise Exception

    def install(self):
        """
        Installs a package into the project folder.
        """
        if self.project_path is None:
            logging.error("Invalid project path")
            raise Exception

        if self.unzipped_path is None and self.zip_path is None:
            self.download()

        if self.unzipped_path is None:
            self._unzip()
    
        # Get file conflicts, warn about them, and backup files
        inters = self._conflict_check()
        for i in inters:
            logging.warning("File '" + "' already exists. Backing up and proceeding.")
            os.rename(i, i + ".bak")

        # Copy all the files making directories as necessary
        files = self.list_files(self.unzipped_path)
        for f in files:
            os.makedirs(os.path.dirname(f), exist_ok=True)
            copyfile(os.path.join(self.unzipped_path, f), os.path.join(self.project_path, f)

    def remove(self):
        """
        Removes a package from the project folder.
        Note: This intentionally does not remove directories.
        """
        files = self._conflict_check()
        for f in files:
            os.remove(f)
        logging.info("You may need to restore backed up files")

    def update(self):
        # TODO see note in download
        pass

    def download(self):
        """
        Downloads a package and saves it in the cache, or uses already cached file.
        """
        filename = self.download_URL.split('/')[-1]
        cache_path = os.path.join(PKG_CACHE, filename)

        if not os.path.exists(PKG_CACHE) or not os.path.isdir(PKG_CACHE):
            os.mkdir(PKG_CACHE)

        # FIXME this caching system will not update files if they have the same name
        if os.path.exists(cache_path):
            self.zip_path = cache_path
        else:
            try:
                if mimetypes.guess_type(self.download_URL) == "application/zip":
                    retrieve(self.download_URL, cachepath) 
                    self.zip_path = cache_path
                else:
                    logging.error("URL provided is not a zip file: " + self.download_path)
                    raise Exception
            except Exception as err
                logging.error("Error downloading package file")
                raise err

    def _unzip(self):
        """
        Unzips the project file into a temporary directory.
        """
        zf = ZipFile(self.zip_path)
        self.unzipped_path = mkdtemp()
        zf.extractall(path=self.unzipped_path)

    def _confilct_check(self):
        """
        Checks for any file conflicts between the package and project.
        """
        proj_files = self._files_list(self.project_path)
        pkg_files = self._files_list(self.unzipped_path)

        return set(proj_files).intersection(pkg_files)

    def _files_list(self, path, absolute=False):
        """
        Gets a list of the relative paths of all the files in a folder.

        @param path: The path to the directory.
        @param absolute: (optional) If True returns a list absolute paths instead.
        """
        if not os.path.exists(path) or not os.path.isdir(path):
            return []
        file_set = set()
        for dir_, _, files in os.walk(path):
            for f in files:
                rel_dir = os.path.relpath(dir_, path)
                rel_file = os.path.join(rel_dir, f)
                if not absolute:
                    file_set.add(rel_file)
                else:
                    file_set.add(os.path.abspath(rel_file))
        return file_set

"""
Module for managing packages. Provides facilites for installing, removing and updating.
"""
import os, sys
from urllib.request import urlretrieve
import mimetypes
import logging
from .base import *
import zipfile
from time import strftime, localtime
from shutil import copyfile
from tempfile import mkdtemp
import validators
from collections import Counter
from pathlib import Path
from .yamltools import *
import re
# A constant for the downloaded package cache
PKG_CACHE = os.path.userexpand("~/.carme-cache")

# Set up logger
FORMAT = 'carme: [%(levelname)s] %(message)s'
logging.basicConfig(level=logging.INFO, format=FORMAT)

class Packager:
    """
    Object for managing a package
    """
    #This specification erroring with Python 3.5. 
    #project_root: str = None
    #zip_path: str = None
    #unzipped_path: str = None
    #download_URL: str = None
    project_root = None
    zip_path = None
    unzipped_path = None
    download_URL = None

    def __init__(self, package_path: str, project_root: str, create=False):
        """
        Creates a new instance of the package object.

        @param package_path: The local path or URL to the package to be installed. Can be to either a folder or a zip archive.
        @param project_root: The local path to the project that the package is going to be installed into.
        """
        #Check if it is a project
        if project_root is None:
            logging.error("Not in a Carme project.")
            exit(1)

        #Set the project root directory
        self.project_root = project_root

        absp = os.path.abspath(package_path)

        # If package_path was a valid URL then download it
        if validators.url(package_path):
            self.download_URL = package_path

        # If the absoulte path of package_path exists as a...
        elif os.path.exists(absp):
        # Folder
            if os.path.isdir(absp):
                self.unzipped_path = absp

            # Zip file
            elif os.path.isfile(absp) and mimetypes.guess_type(absp)[0] == "application/zip":
                self.zip_path = absp

            # Otherwise it was an error and log it
            else:
                raise Exception("Invalid file path or URL: " + package_path)
                print("Download URL:", self.download_URL)

    def create(self, index):
        """
        Create a package from the directory.
        """
        logging.info("Creating package for current project." )
        #get the package name
        package_name=os.path.basename(self.project_root)
        #use the current time
        current_time=strftime("%Y%m%d_%H%M%S", localtime())
        #set the filename for the zip
        filename=package_name+"_"+current_time+".zip"
        self.zip_path=os.path.join(self.project_root,PACKAGES_DIR,filename)
        logging.info("Creating package for current project: "+self.zip_path )

        #Create the package directory if it doesn't exist.
        package_path=Path(os.path.join(self.project_root, PACKAGES_DIR))
        if not package_path.exists():
            print("The packages directory doesn't exist...creating it.")
            os.makedirs(package_path)

        #Load the carmeignore file. This has directories and files which are not to be packaged.
        carmeignore_file = Path(os.path.join(self.project_root, ".carmeignore"))
        if carmeignore_file.exists():
            with open(carmeignore_file) as f:
                carmeignore = f.read().splitlines()
        else:
            ignore=['packages','.git']
        #zip_directory(self.project_root, ignore, self.zip_path)
        if os.path.exists(self.project_root):
            outZipFile = zipfile.ZipFile(self.zip_path, 'w', zipfile.ZIP_DEFLATED)
            # The root directory within the ZIP file.
            rootdir = os.path.basename(self.project_root)
            for dirpath, dirnames, filenames in os.walk(self.project_root):
                for ignore in carmeignore:
                    if ignore in dirnames:
                        dirnames.remove(ignore)
                    if ignore in filenames:
                        filenames.remove(ignore)
                for filename in filenames:
                    #if filename in remove:
                    # Write the file named filename to the archive,
                    # giving it the archive name 'arcname'.
                    filepath   = os.path.join(dirpath, filename)
                    parentpath = os.path.relpath(filepath, self.project_root)
                    arcname = parentpath
                    #arcname    = os.path.join(rootdir, parentpath)
                    #print("filepath:",filepath,"parentpath",parentpath,"arcname",arcname )
                    outZipFile.write(filepath, arcname)
            outZipFile.close()
        if index:
            os.chdir(self.project_root)
            index=os.path.join(os.pardir, DEFAULT_DIR, CONFIG_DIR, INDEX_FILE)
            kwargs=load_yaml_file(index)
            if package_name in kwargs:
                kwargs[package_name]=re.sub(r'\d\d\d\d\d\d\d\d_\d\d\d\d\d\d',current_time, kwargs[package_name])
                logging.info("Updating index: " + kwargs[package_name])
            else:
                kwargs[package_name]=kwargs['default']
                kwargs[package_name]=kwargs[package_name].replace('default', package_name)
                kwargs[package_name]=re.sub(r'\d\d\d\d\d\d\d\d_\d\d\d\d\d\d',current_time, kwargs[package_name])
                logging.info("Creating index: " + kwargs[package_name])
            update_yaml_file(index, kwargs)

    def install(self):
        """
        Installs a package into the project folder.
        """
        if self.project_root is None:
            raise Exception("Invalid project path.")

        if self.unzipped_path is None and self.zip_path is None:
            self.download()

        if self.unzipped_path is None:
            self._unzip()

        # Get file conflicts, warn about them, and backup files
        inters = self._conflict_check()
        for i in inters:
            if i not in MERGE_LIST:
                logging.warning("File '" + i + "' already exists. Backing up and proceeding.")
                os.rename(i, i + ".bak")


        # Copy all the files making directories as necessary
        files = self._files_list(self.unzipped_path)
        for f in files:
            if f in MERGE_LIST and os.path.exists(os.path.join(self.project_root, f)):
                logging.info("Merging the file: "+f)
                merged = merge_yaml(os.path.join(self.project_root, f), os.path.join(self.unzipped_path, f))
                copyfile(merged, os.path.join(self.project_root, f))
            else:
                os.makedirs(os.path.dirname(f), exist_ok=True)
                copyfile(os.path.join(self.unzipped_path, f), os.path.join(self.project_root, f))

        #Add functionaily for merge.
        #add_key('packages', 'azk', self.zip_path, os.path.join(self.project_root, CONFIG_DIR, CONFIG_FILE))

    def remove(self):
        """
        Removes a package from the project folder.
        Note: This intentionally does not remove directories.
        """
        files = self._conflict_check()
        for f in files:
            os.remove(f)
        logging.info("You may need to restore backed up files.")

    def update(self):
        """
        Updates a package
        """
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
                if mimetypes.guess_type(self.download_URL)[0] == "application/zip":
                    urlretrieve(self.download_URL, cache_path)
                    self.zip_path = cache_path
                else:
                    raise Exception("URL provided is not a zip file: " + self.download_URL)
            except Exception as err:
                logging.error("Error downloading package file")
                raise err


    def _unzip(self):
        """
        Unzips the project file into a temporary directory.
        """
        zf = zipfile.ZipFile(self.zip_path)
        self.unzipped_path = mkdtemp()
        zf.extractall(path=self.unzipped_path)

    def _conflict_check(self):
        """
        Checks for any file conflicts between the package and project.
        """
        proj_files = self._files_list(self.project_root)
        pkg_files = self._files_list(self.unzipped_path)

        return set(proj_files).intersection(pkg_files)

    def _files_list(self, path, absolute=False):
        """
        Gets a list of the relative paths of all the files in a folder.

        @param path: The path to the directory.
        @param absolute: (optional) If True returns a list absolute paths instead.
        """

        ignored = [".git", ".gitignore"]

        if not os.path.exists(path) or not os.path.isdir(path):
            return []
        file_set = set()
        for root, dirs, files in os.walk(path, topdown=True):
            dirs[:] = [d for d in dirs if d not in ignored]
            for f in files:
                if f in ignored:
                    continue
                rel_dir = os.path.relpath(root, path)
                rel_file = os.path.join(rel_dir, f)
                if not absolute:
                    file_set.add(rel_file)
                else:
                    file_set.add(os.path.abspath(rel_file))
        return file_set

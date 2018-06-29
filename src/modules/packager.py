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
# A constant for the downloaded package cache
PKG_CACHE = os.path.join(os.path.dirname(sys.modules['__main__'].__file__), 'cache/')

# Set up logger
FORMAT = 'carme: [%(levelname)s] %(message)s'
logging.basicConfig(level=logging.INFO, format=FORMAT)

class Packager:
    """
    Object for managing a package
    """
    project_path: str = None
    zip_path: str = None
    unzipped_path: str = None
    download_URL: str = None

    def __init__(self, package_path: str, project_path: str, create=False):
        """
        Creates a new instance of the package object.

        @param package_path: The local path or URL to the package to be installed. Can be to either a folder or a zip archive.
        @param project_path: The local path to the project that the package is going to be installed into.
        """
        #Check if it is a project
        if project_path is None:
            logging.error("Not in a Carme project.")
            exit(1)
        self.project_path = project_path
        if create:
            self.zip_path=package_path
        else:
            absp = os.path.abspath(package_path)
            index_path=self._check_index(package_path)

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

            elif index_path!=None:
                self.download_URL=index_path
            # Otherwise it was an error and log it
            else:
                raise Exception("Invalid file path or URL: " + package_path)
                print("Download URL:", self.download_URL)

    def create(self):
        """
        Create a package from the directory.
        """
        logging.info("Creating package for current project." )
        package_name=os.path.basename(self.project_path)
        #Create the package directory if it doesn't exist.
        package_path=Path(os.path.join(self.project_path, PACKAGES_DIR))
        if not package_path.exists():
            print("The packages directory doesn't exist...creating it.")
            os.makedirs(package_path)

        #Load the carmeignore file. This has directories and files which are not to be packaged.
        carmeignore_file = Path(os.path.join(self.project_path, ".carmeignore"))
        if carmeignore_file.exists():
            with open(carmeignore_file) as f:
                carmeignore = f.read().splitlines()
        else:
            ignore=['packages','.git']
        #zip_directory(self.project_path, ignore, self.zip_path)
        if os.path.exists(self.project_path):
            outZipFile = zipfile.ZipFile(self.zip_path, 'w', zipfile.ZIP_DEFLATED)
            # The root directory within the ZIP file.
            rootdir = os.path.basename(self.project_path)
            for dirpath, dirnames, filenames in os.walk(self.project_path):
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
                    parentpath = os.path.relpath(filepath, self.project_path)
                    arcname = parentpath
                    #arcname    = os.path.join(rootdir, parentpath)
                    #print("filepath:",filepath,"parentpath",parentpath,"arcname",arcname )
                    outZipFile.write(filepath, arcname)
            outZipFile.close()

    def install(self):
        """
        Installs a package into the project folder.
        """
        if self.project_path is None:
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
            if f in MERGE_LIST and os.path.exists(os.path.join(self.project_path, f)):
                logging.info("Merging the file: "+f)
                merge_yaml(os.path.join(self.project_path, f), os.path.join(self.unzipped_path, f),os.path.join(self.project_path, f))
            else:
                os.makedirs(os.path.dirname(f), exist_ok=True)
                copyfile(os.path.join(self.unzipped_path, f), os.path.join(self.project_path, f))

        #Add functionaily for merge.
        #add_key('packages', 'azk', self.zip_path, os.path.join(self.project_path, CONFIG_DIR, CONFIG_FILE))

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

    def _check_index(self,package_path):
        """
        Checks the presence of a value in the indexself.
        """
        kwargs=load_yaml_file(os.path.join(project_root, CONFIG_DIR, CONFIG_FILE))

        index=load_yaml_url(PACKAGE_INDEX)
        if package_path in index:
            return index[package_path]
        return None


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
        proj_files = self._files_list(self.project_path)
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

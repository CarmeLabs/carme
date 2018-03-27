import os,sys
import logging
from glob import glob
from ruamel.yaml import YAML
from tempfile import NamedTemporaryFile
from random import randint
from pathlib import Path

# set up logging
FORMAT = 'carme: [%(levelname)s] %(message)s'
logging.basicConfig(level=logging.INFO, format=FORMAT, stream=sys.stderr)

def merge_yaml(file1:str, file2:str, outpath=None):
    """
    Merges 2 yaml files returning the path to the merged file.

    @param file1: the path to the first YAML file
    @param file2: the path to the second YAML file
    @param outpath: (optional) the path to the desired output file. Defaults to None in which case a temporary file is used.
    @return: path to file containing the merged YAML
    """

    logging.debug("Merging " + file1 + " with " + file2)

    if not os.path.exists(file1):
        raise FileNotFoundError(file1)
    elif not os.path.isfile(file1):
        raise IsADirectoryError(file1)

    if not os.path.exists(file2):
        raise FileNotFoundError(file2)
    elif not os.path.isfile(file2):
        raise IsADirectoryError(file2)

    with NamedTemporaryFile(delete=False, mode="w+") as outfile:
        logging.debug("Outputting to " + outfile.name)

        # Docker actually doesn't mind duplicate keys in compose files so we are going to abuse that a bit
        # Hopefully if they every change that it will be after docker stack supports multiple files
        outtext = ""
        with open(file1, 'r') as f1:
            outtext += f1.read()
            with open(file2, 'r') as f2:
                outtext += f2.read()
                outfile.write(outtext.strip())

        # get the path, close the file, and return
        return outfile.name

def folder_merge_yaml(folderpath:str, pattern='*.compose.yaml', outpath=None):
    """
    Merges all the YAML files in a directory and its subdirs matching the *.compose.yaml format.

    @param folderpath: path to the folder containing the YAML files to merge
    @param pattern: (optional) a pattern the file has to match. Default '*.compose.yaml'
    @param outpath: (optional) the path to the desired output file. Defaults to None in which case a temporary file is used.
    @return: file object containing the merged YAML
    """

    if not os.path.exists(folderpath):
        raise FileNotFoundError(folderpath)
    if not os.path.isdir(folderpath):
        raise Exception(folderpath + " is not a directory")

    with NamedTemporaryFile(delete=False, mode="w") as outfile:
        files = [y for x in os.walk(folderpath) for y in glob(os.path.join(x[0], pattern))]
        
        for file in files:
            outfile = merge_yaml(outfile.name, file)
            
        # get the path, close the file, and return
        return outfile.name

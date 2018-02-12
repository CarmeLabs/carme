import os
from glob import glob
from ruamel.yaml import YAML
from tempfile import NamedTemporaryFile

def merge_yaml(file1:str, file2:str, outpath=None):
    """
    Merges 2 yaml files returning the path to the merged file.

    @param file1: the path to the first YAML file
    @param file2: the path to the second YAML file
    @param outpath: (optional) the path to the desired output file. Defaults to None in which case a temporary file is used.
    @return: path to the file containing the merged YAML
    """

    if not os.path.exists(file1) or not os.path.exists(file2):
        raise FileNotFoundError

    outfile = None;
    if outpath is not None:
        outfile = open(outpath)
    else:
        outfile = NamedTemporaryFile()

    yaml = YAML()
    f1_yaml = yaml.load(file1)
    f2_yaml = yaml.load(file2)

    yaml.round_trip_dump(f1_yaml, outfile)
    yaml.round_trip_dump(f2_yaml, outfile)

    return outfile.name

def folder_merge_yaml(folderpath:str, pattern='*.compose.yaml', outpath=None):
    """
    Merges all the YAML files in a directory and its subdirs matching the *.compose.yaml format.

    @param folderpath: path to the folder containing the YAML files to merge
    @param pattern: (optional) a pattern the file has to match. Default '*.compose.yaml'
    @param outpath: (optional) the path to the desired output file. Defaults to None in which case a temporary file is used.
    @return: path to the file containing the merged YAML
    """

    if not os.path.exists(folderpath) or not os.isdir(folderpath):
        raise FileNotFoundError

    outfile = None;
    if outpath is not None:
        outfile = open(outpath)
    else:
        outfile = NamedTemporaryFile()
    
    files = [y for x in os.walk(folderpath) for y in glob(os.path.join(x[0], pattern))
    
    for file in files:
        outfile = merge_yaml(outfile, file)

    return outfile.name
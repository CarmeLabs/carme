'''
Converts the Jupyter notebook to a python script, markdown, and restructured text.
'''

import os
import logging
import click
from shutil import copyfile
from ...modules.base import *
import nbformat as nbf
import nbconvert as nbc


# Set up logger
setup_logger()

@click.command()
@click.option('--script', is_flag=True, default=False, help='Convert the notebook to a python script.')
@click.option('--rst', is_flag=True, default=False, help='Convert the notebooks to a reStructuredText output.')
@click.option('--markdown', is_flag=True, default=False, help='Convert the notebooks to a reStructuredText output.')
#@click.option('--all', is_flag=True, default=False, help='Convert the notebooks to a reStructuredText output.')
def convert(script, rst, markdown):
    """
    Launch Jupyter Notebook (using Docker).
    """
    if not script and not rst and not markdown:
        all=True
    else:
        all=False
    project_root=get_project_root()
    notebooks=os.path.join(project_root, NOTEBOOKS_DIR)
    if os.path.isdir(notebooks):
        for dirpath, dirnames, filenames in os.walk(notebooks):
            for filename in filenames:
                if filename.endswith(".ipynb") and os.path.basename(dirpath) != '.ipynb_checkpoints' :
                    parentpath = os.path.relpath(dirpath, notebooks)
                    nb = nbf.read(open(os.path.join(dirpath,filename), 'r'), as_version=4)
                    if rst or all:
                        #EXPORT RST
                        exporter = nbc.RSTExporter()
                        dir=os.path.join(project_root, RST_DIR, parentpath)
                        logging.info("Converting the "+filename+" notebook to an RST format." )
                        _export(nb, exporter, project_root, dir, parentpath,filename, '.rst')
                    if markdown or all:
                        #EXPORT Markdown
                        exporter = nbc.MarkdownExporter()
                        dir=os.path.join(project_root, DOCS_DIR, parentpath)
                        logging.info("Converting the "+filename+" notebook to an Markdown format." )
                        _export(nb, exporter, project_root, dir, parentpath,filename, '.md')
                    if script or all:
                        #EXPORT SCRIPT
                        exporter = nbc.ScriptExporter()
                        dir=os.path.join(project_root, SCRIPTS_DIR, parentpath)
                        logging.info("Converting the "+filename+" notebook to a python script." )
                        _export(nb, exporter, project_root, dir, parentpath,filename, '.py')

                elif filename.endswith(".Rmd"):
                    #TBD add processing for R notebooks. s
                    print("R",filename)

def _export(nb, exporter, project_root, outdir, parentpath, filename, extension):
    #EXPORT RST
    (body, resources) = exporter.from_notebook_node(nb)
    #output the rst file
    print("parent path", parentpath)
    print("outputdir", outdir)
    filename_base=os.path.splitext(filename)[0]
    if not os.path.exists(outdir):
        os.makedirs(outdir)
    with open(os.path.join(outdir,filename_base+extension), "w") as text_file:
        text_file.write(body)

convert
==================

The `carme convert` command will convert all notebooks to markdown, restructured text, and scripts.

The default behavior if issued without flags is to provide all three outputs. However, flags can be added individually to indicate which outputs ones are desired.

Usage
-----

Usage: carme convert [OPTIONS]

  Launch Jupyter Notebook (using Docker).

Options:
  --script    Convert the notebook to a python script.
  --rst       Convert the notebooks to a reStructuredText output.
  --markdown  Convert the notebooks to a reStructuredText output.
  --help      Show this message and exit.

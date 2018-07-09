notebook
==================

The `carme notebook` command mirrors the function of the jupyter lab command, but using Docker containers.

By default, the `carme lab` command will share the current working directory with the container.

Information for the port and image can be pulled from 3 different places and are searched for in this order:

(1) If an image and/or port is passed as an option, that option is used (top priority).
(2) If an image and/or port is set in the config/carme-config.yaml file, that option is used (second priority).
(3) If an image and/or port is set in the (user  home)/.carme/config/carme-config.yaml then  that option will be used (lower priority).

Option 3 is useful to be able to work on multiple projects at once, as it allows you to launch a carme powered docker container from any directory.

Usage
-----

Usage: carme notebook [OPTIONS]

  Launch Jupyter Notebook (using Docker).

Options:
  --image TEXT  The Jupyter docker image (must be based on Jupyter stacks).
  --port TEXT   The Jupyter docker image (must be based on Jupyter stacks).
  --background  Run Docker container in the background.
  --dryrun      Only print the command, do not run.
  --help        Show this message and exit.

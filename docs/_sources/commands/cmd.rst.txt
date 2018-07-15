cmd
==================

The `carme cmd` will combine the configuration settings in /config/<package>.yaml with a templated comand in /cmd/<package>.yaml.  This makes it easy to get up and running with cloud infrasture, as packages typically come configured with defaults.

Usage
-----

Usage: carme cmd [OPTIONS] PACKAGE COMMAND

  Runs commands from the commands folder.

Options:
  --dryrun  Only print the command, do not run.
  --docker  Run the command on the Docker container.
  --server  Run the command on a remote server.
  --yes     Continue multiple commands without waiting.
  --help    Show this message and exit.

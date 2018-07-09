build
==================

The `carme build` command will build all images stored locally in the `docker` directory.

Usage
-----

Usage: carme build [OPTIONS]

  Build project docker images.

Options:
  --force   Force full rebuild without using cache.
  --push    Push image to Dockerhub (must be logged-in).
  --dryrun  Only list build command and don't actually build.
  --help    Show this message and exit.

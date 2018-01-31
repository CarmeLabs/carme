============
Kubelaunch
============

.. image:: https://img.shields.io/pypi/v/hugo_jupyter.svg
        :target: https://pypi.python.org/pypi/carme

.. image:: https://img.shields.io/travis/carme/carme.svg
        :target: https://travis-ci.org/carme/carme

.. image:: https://pyup.io/repos/github/carme/carmeauch-cli/shield.svg
     :target: https://pyup.io/repos/github/carme/carmeauch-cli/
     :alt: Updates

.. image:: https://img.shields.io/github/license/mashape/apistatus.svg


Making analytics-ops on Kubernetes easy.

* Source: https://github.com/carme/carme

This is a work in progress, but the goal is to make 

Installation
------------

.. code-block:: bash

    pip install carme

Usage
-----
Create a new empty directory for your cluster.

.. code-block:: bash

    carme init gcp --jupyter

This will create .

Docker Image
-----
This is a Jupyter Singleuser container with Google Cloud Platform and Azure CLI installed.

Build locally:
```
docker build -t carme/carme:latest -t carme/carme:v0.0.1 .
```
### To use Locally for example.
```
docker run -it --rm -p 8888:8888  -v /Users/<yourpath>/launch:/home/jovyan/work carme/carme:latest /bin/bash
```
### Launch a docker container configured to control.
```
docker run -it --rm -p 8888:8888  carme/carme:latest /bin/bash
```

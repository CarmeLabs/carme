az-z2jh  (Zero to JupyterHub)
=============================

The Zero to Jupyterhub package facilitiates deployment of JupyterHub on Kubernetes. Installing this package will install the AZ-Cluster, JupyterHub, and Jupyter-CPU packages into your project.

Install the AZ-Z2JH package with:

.. code:: ipython3

    carme package install az-z2jh

Usage
-----
Create a Kubernetes cluster with the `AZ-Cluster <https://docs.carme.ai/packages/az-cluster.html>`_ package.

Install JupyterHub with the `JupyterHub <https://docs.carme.ai/packages/jupyterhub.html>`_ package.

Customize the single-user container with the Jupyter-CPU package.

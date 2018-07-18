jupyterhub
==========

This package is installed along with the z2jh package packages (az-z2jh, gcp-z2jh) and requires a Kubernetes cluster.  To install the jupyterhub package individually you can use:

.. code:: ipython3

    carme package install jupyterhub

The jupyterhub package is designed to install Jupyterhub on any Kubernetes instance.

From the notebook included in the package:


Before you Begin. The '--dryrun' option and the '--yes' Option
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

| Do you want to run the commands or just see them?
| Below we have set the carme option ``dryrun`` so that commands are
  printed and not executed.

If executing carme commands from the command line, by default the CMD
command and will print the command and ask you to confirm before
executing it. In Jupyter notebooks, this interactivity isn't possible.
Instead, just add the --yes flag.

.. code:: ipython3

    #To run for real, just set dryrun=''
    #dryrun= '' to run or dryrun='--dryrun' to print. 
    dryrun=''
    yes = '--yes'

Jupyterhub on Kubernetes
~~~~~~~~~~~~~~~~~~~~~~~~

This notebook can be used to launch a standard instance of Jupyterhub
which includes a proxy server, and an instance of Jupyterhub.

This assumes you have a lauchfile in your working directory and have a
Kubernetes cluster already loaded.

Print Jupyterhub Commmands
~~~~~~~~~~~~~~~~~~~~~~~~~~

Optionally you can print the configuration and common commands for your
desired cluster. You can use this as a reference and copy and paste into
the terminal.

.. code:: ipython3

    carme cmd jupyterhub list

Initialize Jupyterhub Configuration File
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The following will initialize Jupyterhub configuration in the
/config//config.yaml

.. code:: ipython3

    #Clone the Jupyterhub repo.
    carme cmd jupyterhub init  

Install Jupyterhub
~~~~~~~~~~~~~~~~~~

This will install the jupyterhub instance.

.. code:: ipython3

    carme cmd jupyterhub install  

Check the Jupyterhub IP
~~~~~~~~~~~~~~~~~~~~~~~

This will get the public IP of the Jupyterhub service.

.. code:: ipython3

    carme cmd jupyterhub get_ip  

Update Authorization
~~~~~~~~~~~~~~~~~~~~

TBD

.. code:: ipython3

    carme app jupyter jup_dummy_auth


.. code:: ipython3

    carme app jupyter jup_admin

Updata Jupyterhub
~~~~~~~~~~~~~~~~~

TBD

.. code:: ipython3

    #Upgrading Jupyterhub 
    carme cmd jupyterhub upgrade  

Cleanup the Installation
~~~~~~~~~~~~~~~~~~~~~~~~

This will cleanup the installation, deleting the instance of Jupyterhub.

.. code:: ipython3

    #Upgrading Jupyterhub 
    carme cmd jupyterhub delete  

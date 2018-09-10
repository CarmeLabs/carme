az-server (CPU/GPU)
===================

The server package is designed to provide a server infra

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
    dryrun='--dryrun' 
    #Because Jupyter notebooks aren't interactive, commands have to be executed with a '--yes' option. 
    yes = '--yes'   #Needed only for Jupyter notebooks. 
    
    


Manage a Server on Azure
~~~~~~~~~~~~~~~~~~~~~~~~

This notebook can be used to launch a server using Azure CLI. It is
designed to be run via the included Docker container, but it can be run
locally if the appropriate tools are installed.

This script assumes you have already installed the az-server package and
logged in using the ``az login`` command.

To install the package use: ``carme package install az-server``

To log into the Azure CLI: ``carme cmd az-server login``

You may also have to set the correct subscription.
``az account list --refresh --output table``

Set the appropriate subscription here.
``az account set -s <YOUR-CHOSEN-SUBSCRIPTION-NAME>``

.. code:: ipython3

    carme cmd az-server login   

Print Available Commands
~~~~~~~~~~~~~~~~~~~~~~~~

Optionally you can print the configuration and common commands for your
desired cluster. You can use this as a reference and copy and paste into
the terminal.

.. code:: ipython3

    carme cmd az-server list


Review the Package Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You should always review your configuration prior to executing any
commands.

.. code:: ipython3

    cat ../../config/az-server.yaml

Create Resource Groups
~~~~~~~~~~~~~~~~~~~~~~

Google calls them projects. Azure calles them resource groups. Either
way you need one. This useful to track spending and also ensure you
delete all resources at the end.

.. code:: ipython3

    carme cmd az-server create_group  

Create the Server
~~~~~~~~~~~~~~~~~

This will create the server with an SSH key. This is the easiest way to
manage it.

.. code:: ipython3

    carme cmd az-server create  

WAIT FOR A WHILE
~~~~~~~~~~~~~~~~

This can take a few minutes.

Open Ports on the Target Machine
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

There is a need to open ports on the target machine.

.. code:: ipython3

    #gcloud container clusters get-credentials carme
    carme cmd az-server open_port_8888  

Using and Enhancing Your Server
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``carme cmd az-server ssh --dryrun``

.. code:: ipython3

    carme cmd az-server ssh  

Stop the Server
~~~~~~~~~~~~~~~

The stop command by default deallocates so you won't be charged untill
you start it up again.

.. code:: ipython3

    #Scale the cluster 
    carme cmd az-server stop  

Start the Server
~~~~~~~~~~~~~~~~

.. code:: ipython3

    #Stop the cluster, effectively setting the size to 0.
    carme cmd az-server start  

Show the Server
~~~~~~~~~~~~~~~

.. code:: ipython3

    #Set the cluster to the normal size.
    carme cmd az-server show  

Deleting the Server
~~~~~~~~~~~~~~~~~~~

This will delete the Kubernetes cluster by deleting the entire project.
This will prefent any future charges.

.. code:: ipython3

    #Always delete the namespace first. 
    carme cmd az-server delete  

Delete the Resource Group
~~~~~~~~~~~~~~~~~~~~~~~~~

To fully clean up everything, go ahead and delete the resource group.

.. code:: ipython3

    carme cmd az-server delete_resource_group  

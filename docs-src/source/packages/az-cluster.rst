az-cluster (Kubernetes)
=======================

The cluster package is designed to provide a Kubernetes cluster, useful for providing workgroups and classrooms access to Juypter.

This package is installed along with the az-z2jh package.  To nstall the az-cluster package individually you can use:

.. code:: ipython3

    carme package install az-cluster

If running on the Azure Cloud Shell, (1) install carme, (2) verify the configuration file, and (3) ensure the correct subscription is set. Then the cluster can be created using one command:

.. code:: ipython3

    carme cmd az-cluster create_all

The above will step through the relevant steps of the notebook below.

.. code:

    carme cmd az-cluster install_helm

Alternately, the commands can be run directly from the notebook included with the package.

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

View Available Commands
~~~~~~~~~~~~~~~~~~~~~~~

.. code:: ipython3

    carme cmd az-cluster list


View the Configuration
~~~~~~~~~~~~~~~~~~~~~~

.. code:: ipython3

    carme cmd az-cluster show_config 

Create Kubernetes Cluster on Azure
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This notebook can be used to launch a Kubernetes Cluster using Azure
CLI. It is designed to be run in an environment in whic the appropriate
tools (Helm/Azure CLI) are installed.

This script assumes you have already installed the az-server package and
logged in using the ``az login`` command.

To install the package use: ``carme package install az-cluster``

To log into the Azure CLI: ``carme cmd az-cluser login``

You may also have to set the correct subscription.
``az account list --refresh --output table``

Set the appropriate subscription here.
``az account set -s <YOUR-CHOSEN-SUBSCRIPTION-NAME>``

Login to Azure
~~~~~~~~~~~~~~

.. code:: ipython3

    carme cmd az-cluster login  

List Available Subscription (Optional)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can update the current subscription usine either the ID or the name.

.. code:: ipython3

    #This will list all subscrptions. 
    carme cmd az-cluster list_subscriptions  

Set the Appropriate Subscription (Optional)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can skip this if you already have the appropriate subscription set.

.. code:: ipython3

    carme cmd az-cluster set_subscription  

Create the Resource Group
~~~~~~~~~~~~~~~~~~~~~~~~~

Google calls them projects. Azure calles them resource groups. Either
way you need one. This useful to track spending and also ensure you
delete all resources at the end.

.. code:: ipython3

    carme cmd az-cluster create_group  

Enable the Cloud API
~~~~~~~~~~~~~~~~~~~~

The following commands enable various Azure tools that we’ll need in
creating and managing the JupyterHub.

.. code:: ipython3

    carme cmd az-cluster register  

Create the ssh key.
~~~~~~~~~~~~~~~~~~~

This will create the ssh key and put it in the ./config/ssh/servername
directory.

.. code:: ipython3

    carme cmd az-cluster create_key  

Create the Cluster
~~~~~~~~~~~~~~~~~~

This will create your Kubernetes Cluster. You have to wait for about 5
minutes before this finishes creating.

.. code:: ipython3

    carme cmd az-cluster create  

WAIT FOR A WHILE
~~~~~~~~~~~~~~~~

This can take up to 10 minutes.

If you get an error ".kube/config: No such file or directory" just wait,
it is likely still booting up.

Get Credentials for Kubectl
~~~~~~~~~~~~~~~~~~~~~~~~~~~

We need to add the credentials for Kubectl to work. You need a bit of
time for your Kubernetes to launch.

.. code:: ipython3

    carme cmd az-cluster get_credentials  

Check your Cluster
~~~~~~~~~~~~~~~~~~

``kubectl`` is the default kubernetes command you can use to check out
lots of things on your cluster. Go ahead and trying the ``cluster info``
and ``get node`` commands below.

.. code:: ipython3

    kubectl cluster-info

.. code:: ipython3

    kubectl get node

Helm Installation.
~~~~~~~~~~~~~~~~~~

We are going to be utilizing Helm for installations of a variety of
analytics tools. This command will install Tiller on your cluster. As
they say, "Happy Helming"

The command will created the service account, initiate it, and print the
helm version.

.. code:: ipython3

    
    kubectl --namespace kube-system create serviceaccount tiller

.. code:: ipython3

    helm init --service-account tiller

A critical factor for Helm is that you have the same version running
locally and via your machine. If you run helm version and you the same
versions on the client and sever, you should be fine.

*Client: &version.Version{SemVer:"v2.6.2",
GitCommit:"be3ae4ea91b2960be98c07e8f73754e67e87963c",
GitTreeState:"clean"}*

*Server: &version.Version{SemVer:"v2.6.2",
GitCommit:"be3ae4ea91b2960be98c07e8f73754e67e87963c",
GitTreeState:"clean"}*

.. code:: ipython3

    helm version

Secure Helm

.. code:: ipython3

    # Secure Helm
    kubectl --namespace=kube-system patch deployment tiller-deploy --type=json --patch='[{"op": "add", "path": "/spec/template/spec/containers/0/command", "value": ["/tiller", "--listen=localhost:44134"]}]'

Resize a Cluster
~~~~~~~~~~~~~~~~

The commands below can be used to resize the cluster. For example, you
man need to scale up for classroom exercises. This is held in the config
file as the number of servers for class\_size.

.. code:: ipython3

    carme cmd az-cluster class_size  

Stop the cluster, effectively setting the size to 0.

.. code:: ipython3

    carme cmd az-cluster stop  


.. parsed-literal::

    carme: [INFO] All cmd commands issued from project root directory to ensure relative path consistency.
    Traceback (most recent call last):
      File "/anaconda3/envs/carme/bin/carme", line 11, in <module>
        load_entry_point('carme', 'console_scripts', 'carme')()
      File "/anaconda3/envs/carme/lib/python3.6/site-packages/click/core.py", line 722, in __call__
        return self.main(*args, **kwargs)
      File "/anaconda3/envs/carme/lib/python3.6/site-packages/click/core.py", line 697, in main
        rv = self.invoke(ctx)
      File "/anaconda3/envs/carme/lib/python3.6/site-packages/click/core.py", line 1066, in invoke
        return _process_result(sub_ctx.command.invoke(sub_ctx))
      File "/anaconda3/envs/carme/lib/python3.6/site-packages/click/core.py", line 895, in invoke
        return ctx.invoke(self.callback, **ctx.params)
      File "/anaconda3/envs/carme/lib/python3.6/site-packages/click/core.py", line 535, in invoke
        return callback(*args, **kwargs)
      File "/Users/jasonkuruzovich/githubdesktop/0_class/carme/src/cli/commands/cmd.py", line 48, in cmd
        elif isinstance(commands[command], ruamel.yaml.comments.CommentedSeq):
      File "/anaconda3/envs/carme/lib/python3.6/site-packages/ruamel/yaml/comments.py", line 702, in __getitem__
        return ordereddict.__getitem__(self, key)
    KeyError: 'stop'


Set the cluster to the normal size. This is a "non class time" size.

.. code:: ipython3

    #Set the cluster to the normal size.
    carme cluster normal_size

Deleting a Kubernetes Cluster
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This will delete the Kubernetes cluster by deleting the entire project.
This will prefent any future charges.

.. code:: ipython3

    #Always delete the namespace first. 
    carme cmd az-cluster delete  

Delete the Resource Group
~~~~~~~~~~~~~~~~~~~~~~~~~

To fully clean up everything, go ahead and delete the resource group.

.. code:: ipython3

    carme cmd az-cluster delete_group  

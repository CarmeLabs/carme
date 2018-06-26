


Installation
============

Install Python3 via [python.org](https://www.python.org/downloads/)` or [Miniconda](https://conda.io/miniconda.html) or [Anaconda](https://www.anaconda.com/download/) and `pip` using the recommended method for your platform.

Install Carme

.. code:: bash

    pip install git+https://github.com/CarmeLabs/carme


Update Carme
============
We are currently making lots of updates.

.. code:: bash

    pip install git+https://github.com/CarmeLabs/carme --upgrade


Install Docker
==============
You will also need Docker in order to use Carme.  Here is how you [get Docker](https://www.docker.com/get-docker).

.. code:: bash

    pip install git+https://github.com/CarmeLabs/carme


Developer Installation Instructions
===================================
Clone the Repository
Clone the github repository:

.. code:: bash

    git clone https://github.com/CarmeLabs/carme
    cd carme


For Conda/Miniconda, then run:

.. code:: bash

    conda create --name carme
    source activate carme
    conda install -c anaconda pip
    pip install -e .


For individuals running (pure) Python:

.. code:: bash

    python3 -m venv carme-env
    source bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
    pip install -e .


Running Tests
=============

.. code:: bash

    python setup.py test

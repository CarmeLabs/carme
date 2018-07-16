# Carme
The **C**ontainerized **A**nalytics **R**untime and **M**anagement **E**ngine.

## About
Carme is framework which enables data scientists to create and deploy AI applications.  Carme attempts to take the pain out projects by facilitating common tasks relevant to the majority of analytics teams, such as:
- Use Jupyter, Jupyterlab, and Jupyterhub setup in a container-based environment.
- Simplified version control for data and models for increased reproducibility.
- Directed acyclic graph (DAG) creation, monitoring, and deployment for data pipelines.
- Setup of cluster and GPU infrastructure for scaling analyses.
- Starter notebooks for best-of-class deep learning analyses.
- Dash and Bokeh data application deployment.

Carme can improve workflows for individuals, teams, as well as data science classrooms.

## Installation Instructions

### Via Script
```
$ curl https://raw.githubusercontent.com/carmelabs/carme/master/scripts/get > get_helm.sh
$ chmod 700 get_carme.sh
$ ./get_carme.sh
```
### Install Python
Install Python3 via [python.org](https://www.python.org/downloads/)` or [Miniconda](https://conda.io/miniconda.html) or [Anaconda](https://www.anaconda.com/download/) and `pip` using the recommended method for your platform.

### Install Carme
```
pip install git+https://github.com/CarmeLabs/carme
```

### Install Docker
You will also need Docker in order to use Carme.  Here is how you [get Docker](https://www.docker.com/get-docker).


## Developer Installation Instructions

### Clone the Repository
Clone the github repository:
```
git clone https://github.com/CarmeLabs/carme
cd carme
```
### Install Carme in Development Mode

For Conda/Miniconda, then run:
```
conda create --name carme
source activate carme
conda install -c anaconda pip
pip install -r requirements.txt
pip install -e .
```

For individuals running Python on Azure Cloud Shell or Google Cloud:
```
python3 -m venv carme-env
source carme-env/bin/activate
cd carme
pip3 install --upgrade pip
pip3 install -r requirements.txt
pip3 install -e .
```

Or with a script:

```
wget https://raw.githubusercontent.com/CarmeLabs/carme/master/scripts/get/get_carme_dev.sh
wget https://raw.githubusercontent.com/CarmeLabs/carme/master/scripts/get/activate.sh
source get_carme_dev.sh
```

Test that it is working with:

```
carme --help
```



### Running Tests
`python setup.py test`

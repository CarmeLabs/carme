#THIS IS AN EARLY PROJECT.

# Carme
The **C**ontainerized **A**nalytics **R**untime and **M**anagement **E**ngine.  Carme is also a moon of Jupyter.

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

### Install Python
Install Python3 via [python.org](https://www.python.org/downloads/) or [Miniconda](https://conda.io/miniconda.html) or [Anaconda](https://www.anaconda.com/download/) and `pip` using the recommended method for your platform.

### Install Carme with Conda
The easiest way to get Carme with conda is with this script.
```
wget https://raw.githubusercontent.com/CarmeLabs/carme/master/scripts/get/get_carme_conda.sh
source get_carme_conda.sh
```
Alternately, you can use the following series of commands.
```
conda create --name carme-env --yes
source activate carme-env
conda install -c anaconda pip --yes
wget https://raw.githubusercontent.com/CarmeLabs/carme/master/requirements.txt
pip uninstall carme --yes
pip install -r requirements.txt
pip install git+https://github.com/CarmeLabs/carme.git
rm requirements.txt
```
### Installing with Python Virtual Environment
Alternate, if using pure Python you can use Python virtual environments.  This script will install carme.
```
wget https://raw.githubusercontent.com/CarmeLabs/carme/master/scripts/get/get_carme.sh
source get_carme.sh
```
Alternately, you can enter the commands below.
```
python3 -m venv carme-env
source carme-env/bin/activate
wget https://raw.githubusercontent.com/CarmeLabs/carme/master/requirements.txt
pip3 install -r requirements.txt
pip3 install git+https://github.com/CarmeLabs/carme.git
```

## Install Docker
You will also need Docker in order to use Carme.  Here is how you [get Docker](https://www.docker.com/get-docker).

## Developer Installation Instructions

### Install Carme in Developer Mode with Conda
```
git clone https://github.com/CarmeLabs/carme
cd carme
conda create --name carme-env --yes
source activate carme-env
conda install -c anaconda pip --yes
pip uninstall carme --yes
pip install -r requirements.txt
pip install -e .
```
### Installing in Developer Mode with Python Virtual Environment
```
git clone https://github.com/CarmeLabs/carme
cd carme
python3 -m venv carme-env
source carme-env/bin/activate
pip3 install -r requirements.txt
pip3 install -e .
```

### Running Tests
`python setup.py test`

# Carme
The **C**ontainerized **A**nalytics **R**untime and **M**anagement **E**ngine.

## About
Carme is framework which enables data scientists to create and deploy data applications.  Carme attempts to take the pain out projects by facilitating common tasks relevant to the majority of analytics teams, such as:
- Use Jupyter, Jupyterlab, and Jupyterhub setup in a container-based environment.
- Simplified version control for data and models for increased reproducibility.
- Directed acyclic graph (DAG) creation, monitoring, and deployment for data pipelines.
- Setup of cluster and GPU infrastructure for scaling analyses.
- Starter notebooks for best-of-class deep learning analyses.
- Dash and Bokeh data application deployment.

Carme can improve workflows for individuals, teams, as well as data science classrooms.

## Installation Instructions

### Install Python
Install Python3 via [python.org](https://www.python.org/downloads/)` or [Miniconda](https://conda.io/miniconda.html) or [Anaconda](https://www.anaconda.com/download/) and `pip` using the recommended method for your platform.

### Install Carme
```
pip install git+https://github.com/CarmeLabs/carme
```
### Update Carme
We are currently making lots of updates.
```
pip install git+https://github.com/CarmeLabs/carme --upgrade
```

### Install Docker
You will also need Docker in order to use Carme.  Here is how you [get Docker](https://www.docker.com/get-docker).

```
pip install git+https://github.com/CarmeLabs/carme
```

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
pip install -e .
```

For individuals running (pure) Python:
```
python3 -m venv carme-env
source bin/activate
pip install --upgrade pip
pip install -r requirements.txt
pip install -e .
```

### Running Tests
`python setup.py test`

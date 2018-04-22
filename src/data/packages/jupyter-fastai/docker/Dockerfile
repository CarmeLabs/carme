FROM jupyter/scipy-notebook:latest
LABEL maintainer "Carmelabs"
ENV LANGUAGE en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LC_ALL en_US.UTF-8
ENV LC_CTYPE en_US.UTF-8
ENV LC_MESSAGES en_US.UTF-8
USER root
COPY config/* /tmp/config/

RUN apt-get update && cat /tmp/config/packages.txt | xargs apt-get install -y --allow-downgrades --no-install-recommends
USER $NB_UID
RUN pip install --upgrade pip
#Solution 1
RUN conda config --add channels fastai && conda config --add channels pytorch  && conda config --add channels peterjc123
RUN conda install --yes --file /tmp/config/conda-requirements.txt
RUN pip install -r /tmp/config/pip-requirements.txt
RUN jupyter serverextension enable --py nbgitpuller --sys-prefix
RUN conda update --yes jupyter jupyterlab
RUN jupyter labextension install @jupyterlab/google-drive
RUN jupyter labextension install @jupyterlab/github

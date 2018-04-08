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
USER jovyan

#Solution 1
RUN conda config --add channels fastai && conda config --add channels pytorch  && conda config --add channels peterjc123
RUN conda install --yes --file /tmp/config/conda-requirements.txt
RUN pip install -r /tmp/config/pip-requirements.txt

#Potential Solution 2
#RUN cd /tmp/config && /opt/conda/bin/conda env create -f /tmp/config/environment-cpu.yml
#RUN /opt/conda/bin/conda clean -ya && /bin/bash -c "source activate fastai-cpu && python -m ipykernel install --user --name fastai-cpu --display-name 'Python3 (fast-ai)'"

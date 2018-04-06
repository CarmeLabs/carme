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

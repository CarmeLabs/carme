FROM jupyter/base-notebook:latest
LABEL maintainer "Carmelabs"
ENV LANGUAGE en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LC_ALL en_US.UTF-8
ENV LC_CTYPE en_US.UTF-8
ENV LC_MESSAGES en_US.UTF-8
USER root
COPY config/* /tmp/config/
RUN apt-get update && cat /tmp/config/packages.txt | xargs apt-get install -y --allow-downgrades --no-install-recommends
#         && sed -i 's/^# en_US.UTF-8 UTF-8$/en_US.UTF-8 UTF-8/g' /etc/locale.gen \
#         && locale-gen \
#         && update-locale LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8 \
USER jovyan
RUN cd /tmp/config && /opt/conda/bin/conda env create environment.yml
RUN /opt/conda/bin/conda clean -ya

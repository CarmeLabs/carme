#!/bin/bash
echo "Checking for CUDA and installing."
# Check for CUDA and try to install.
if ! dpkg-query -W cuda-8-0; then
  #download CUDA and some Docker Prerequisites.
  curl -O https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1604/x86_64/cuda-repo-ubuntu1604_8.0.61-1_amd64.deb
  dpkg -i ./cuda-repo-ubuntu1604_8.0.61-1_amd64.deb
  apt-get update
  apt-get install cuda-8-0
fi
echo "Checking for Docker-CE and Installing."
if ! dpkg-query -W docker-ce; then
  #download docker
  curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
  apt-key fingerprint 0EBFCD88
  add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
  apt-get update
  #install prerequisites
  apt-get install apt-transport-https ca-certificates curl software-properties-common python3-pip -y
  apt-get install docker-ce -y
  curl -L https://github.com/docker/compose/releases/download/1.21.0/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose
  chmod +x /usr/local/bin/docker-compose
fi
echo "Checking for NVIDIA Docker and installing."
if ! dpkg-query -W nvidia-docker2; then
  curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
  distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
  curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | tee /etc/apt/sources.list.d/nvidia-docker.list
  apt-get update
  apt-get install nvidia-docker2 -y
  pkill -SIGHUP dockerd
fi

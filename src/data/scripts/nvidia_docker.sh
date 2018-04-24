#!/bin/bash
echo "Checking for Docker-CE and Installing."
if ! dpkg-query -W docker-ce; then
  #download docker
  curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
  apt-key fingerprint 0EBFCD88
  add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
  apt-get update
  #install prerequisites
  apt-get install -y apt-transport-https ca-certificates curl software-properties-common
  apt-get install -y docker-ce
  curl -L https://github.com/docker/compose/releases/download/1.21.0/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose
  chmod +x /usr/local/bin/docker-compose
fi

#!/bin/bash

# this script automatically installs docker on an Ubuntu 18.04 machine.

# update package index
sudo apt-get update

# uninstall possible old versions
sudo apt-get remove docker docker-engine docker.io containerd runc -y

sudo apt-get install apt-transport-https ca-certificates curl gnupg-agent software-properties-common

# add GPG key
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

# set up stable repository
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"

# update package index
sudo apt-get update

# install
sudo apt-get install docker-ce docker-ce-cli containerd.io -y




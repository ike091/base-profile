#!/bin/bash

# installs minikube and virtualbox (Ubuntu 18.04)

sudo apt-add-repository deb [arch=amd64] "https://download.virtualbox.org/virtualbox/debian bionic contrib"

wget -q https://www.virtualbox.org/download/oracle_vbox_2016.asc -O- | sudo apt-key add -

sudo apt-get update
sudo apt-get install virtualbox-6.1


curl -Lo minikube https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64 && chmod +x minikube

sudo mkdir -p /usr/local/bin/
sudo install minikube /usr/local/bin/
sudo rm minikube

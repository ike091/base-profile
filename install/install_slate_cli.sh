#!/bin/bash

# Installs the slate client on an Ubuntu machine.

sudo curl -LO https://jenkins.slateci.io/artifacts/client/slate-linux.tar.gz
sudo tar xzf slate-linux.tar.gz
sudo mv slate /usr/local/bin
sudo rm slate-linux.tar.gz

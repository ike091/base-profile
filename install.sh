#!/bin/bash

# this bash script installs necessary software on all nodes

# update package index
sudo apt update

# install snmp
sudo apt install snmp -y

# install tool for managing mib data
sudo apt install snmp-mibs-downloader -y

# install snmp daemon
sudo apt install snmpd -y

# copy configuration file
sudo cp /local/repository/snmpd.conf /etc/snmp/snmpd.conf

# copy .vimrc on each VM (provides useful remappings)
cp /local/repository/.vimrc ~/

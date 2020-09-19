#!/bin/bash

# This bash script configures an Ubuntu SNMP manager.

# update package index
sudo apt update

# install snmp and tool for managing mib data
sudo apt install snmp snmp-mibs-downloader -y

# update configuration file
sudo cp /local/repository/config/snmp.conf /etc/snmp/snmp.conf

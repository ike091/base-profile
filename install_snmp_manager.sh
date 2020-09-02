#!/bin/bash

# This bash script configures an Ubuntu SNMP manager.

# update package index
sudo apt update

# install snmp and tool for managing mib data
sudo apt install snmp snmp-mibs-downloader -y

# install snmp daemon
# sudo apt install snmpd -y

# copy configuration file
# sudo cp /local/repository/snmpd.conf /etc/snmp/snmpd.conf

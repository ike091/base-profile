#!/bin/bash

# This bash script configures an Ubuntu SNMP agent.

# update package index
sudo apt update

# install snmp
# sudo apt install snmp -y

# install snmp daemon
sudo apt install snmpd -y

# copy configuration file
sudo cp /local/repository/config/snmpd.conf /etc/snmp/snmpd.conf

# start service
sudo service snmpd start

# restart service (seems to be needed for non-default configuration to load)
sudo service snmpd restart

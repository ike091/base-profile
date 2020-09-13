#!/bin/bash

# Installs telegraf on an Ubuntu machine.

wget https://dl.influxdata.com/telegraf/releases/telegraf_1.15.2-1_amd64.deb

sudo dpkg -i telegraf_1.15.2-1_amd64.deb

# stop the service, as it automatically starts
sudo service telegraf stop

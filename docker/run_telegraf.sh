#!/bin/bash

# starts the telegraf service with the baked in config file
# telegraf --config /usr/src/app/telegraf.conf

# starts the telegraf service wtih the config file from k8s/helm
telegraf --config /etc/config/telegraf.conf

# run until container shuts down
while true; do sleep 1000; done

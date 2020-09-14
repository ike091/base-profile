#!/bin/bash

# starts the telegraf service
telegraf --config /usr/src/app/telegraf.conf

while true; do sleep 1000; done

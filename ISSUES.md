# Issues

## Features:
* Pass in custom Telegraf configuration file
* Custom Telegraf SNMP interface (choose hosts to monitor, custom OID list)
* Web-based viewing of log files 
* Stream logs to database

## To-do:
* Modify chart such that the Telegraf configuration file is not baked into the Docker container image.
* Figure out if any templates under `helm/old/` are needed

## Bugs:
* Telegraf configuration file is baked into container image.

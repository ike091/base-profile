# use ubuntu 18.04 as the base image
FROM ubuntu:18.04

# install software to install telegraf
RUN apt-get update \
&& apt-get install -y wget \
&& apt-get install -y dpkg

# install SNMP and SNMP MIB tool
RUN apt-get install -y snmp snmp-mibs-downloader

# install telegraf
RUN wget https://dl.influxdata.com/telegraf/releases/telegraf_1.15.2-1_amd64.deb \
&& dpkg -i telegraf_1.15.2-1_amd64.deb \
&& rm telegraf_1.15.2-1_amd64.deb

# set a working directory for this app
WORKDIR /usr/src/app

# copy files into container
COPY . .

# copy telegraf configuration file into proper location
# COPY ./telegraf.conf /etc/telegraf/telegraf.conf

# start the telegraf service
# CMD ["telegraf", "--config", "./telegraf.conf"]
# CMD ["service", "telegraf", "start"]

# expose required ports here (191?)
EXPOSE 161

# use ubuntu 18.04 as the base image
FROM ubuntu:18.04

# install software to install telegraf
RUN apt-get update && apt-get install -y wget
RUN apt-get install -y dpkg

# install telegraf
RUN wget https://dl.influxdata.com/telegraf/releases/telegraf_1.15.2-1_amd64.deb
RUN dpkg -i telegraf_1.15.2-1_amd64.deb

# set a working directory for this app
WORKDIR /usr/src/app

# copy files into container
COPY . .

# expose required ports here (191?)
EXPOSE 191

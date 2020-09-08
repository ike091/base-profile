
# use ubuntu 18.04 as the base image
FROM ubuntu:18.04

# set a directory for this app
WORKDIR /usr/src/app

# copy files into container
COPY . .

# install telegraf
RUN sh install_telegraph.sh

# expose required ports here (191?)
EXPOSE 191

FROM ubuntu:latest

RUN apt-get update

ADD --chown=root ./app/ras /ras
ADD --chown=root ./app/server_info.txt /server_info.txt

WORKDIR /

ENTRYPOINT /ras


FROM ubuntu:latest

RUN apt-get update

ADD --chown=root ./app/main /main
ADD --chown=root ./app/dev_journal.txt /dev_journal.txt
ADD --chown=root ./app/templates /templates

WORKDIR /

ENTRYPOINT /main

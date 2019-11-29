FROM ubuntu:latest

RUN apt-get update 


ADD --chown=root ./main /main
ADD --chown=root ./templates/ /templates/

WORKDIR /

ADD run.sh /

RUN chmod 555 /run.sh

ENTRYPOINT /run.sh

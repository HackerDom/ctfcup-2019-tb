FROM ubuntu:latest

RUN apt-get update && apt-get upgrade -yyq
RUN apt-get install socat -yyq

ADD --chown=root ./ras /main
ADD --chown=root ./server_info.txt /server_info.txt
ADD --chown=root ./run.sh /run.sh

WORKDIR /

ENTRYPOINT /run.sh

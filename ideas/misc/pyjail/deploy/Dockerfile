FROM ubuntu:latest

RUN apt-get update && apt-get install -y python-pip python-dev

ADD --chown=root ./app/main.py /asdqew123123zxcsad.py
ADD --chown=root ./app/secret_report.txt /secret_report.txt
ADD --chown=root ./app/run.sh /run.sh

WORKDIR /

ENTRYPOINT /run.sh

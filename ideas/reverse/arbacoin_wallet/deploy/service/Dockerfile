FROM ubuntu:latest

RUN apt-get update && apt-get upgrade -yyq
RUN apt-get install socat -yyq
RUN apt-get install python -yyq

ADD --chown=root ./server.py /server.py
ADD --chown=root ./wallet_gen.py /wallet_gen.py
ADD --chown=root ./run.sh /run.sh
ADD --chown=root ./serve.sh /serve.sh

WORKDIR /

ENTRYPOINT /serve.sh

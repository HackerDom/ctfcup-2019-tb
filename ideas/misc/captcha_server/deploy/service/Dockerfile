FROM ubuntu:latest
# imagegen.py  micross.ttf  modify.png  msg.py  run.sh  server.py  template.png

RUN apt-get update && apt-get upgrade -yyq
#RUN apt-get install socat -yyq
RUN apt-get install python python-pip -yyq
RUN pip install Pillow 

ADD --chown=root ./imagegen.py /imagegen.py
ADD --chown=root ./micross.ttf /micross.ttf
ADD --chown=root ./modify.png /modify.png
ADD --chown=root ./msg.py /msg.py
ADD --chown=root ./run.sh /run.sh
ADD --chown=root ./server.py /server.py
ADD --chown=root ./template.png /template.png


WORKDIR /

ENTRYPOINT /run.sh

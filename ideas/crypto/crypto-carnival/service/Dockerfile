FROM python:3.6

RUN apt update && \
    apt install -y socat libgmp3-dev

RUN useradd -s /bin/false -m task

WORKDIR /home/task/

ADD requirements.txt ./

RUN pip install -r requirements.txt

ADD server.py ui.py flag.txt ./
ADD ciphers/* ./ciphers/

RUN chmod 555 server.py && \
    chmod 444 flag.txt ui.py ciphers/*

ENTRYPOINT ["socat", "TCP-LISTEN:31337,reuseaddr,fork", "EXEC:'./server.py',su=task"]

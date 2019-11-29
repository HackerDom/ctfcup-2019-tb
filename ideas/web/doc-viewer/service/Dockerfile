FROM keltecc/nsjail:latest

RUN apt update && \
    apt install -y python3 python3-pip

COPY requirements.txt /app/

RUN python3 -m pip install -r /app/requirements.txt

ADD . /app

ADD nsjail/nsjail.sh /nsjail.sh

RUN chmod 555 /nsjail.sh && \
    chmod 444 /app/flag.txt

WORKDIR /app/

ENTRYPOINT ["/nsjail.sh"]
CMD [ "/usr/local/bin/gunicorn", "-b", "0.0.0.0:9999", "-w", "4", "wsgi:app" ]


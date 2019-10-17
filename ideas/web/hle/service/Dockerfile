FROM python:3.7

RUN apt-get update
RUN apt-get install -y xinetd && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

ENV PYTHONUNBUFFERED 1

RUN mkdir -p /app
COPY . /app
WORKDIR /app

RUN pip3 install -r requirements.txt

COPY ./hell.xinetd /etc/xinetd.d/hell

RUN chmod 400 /etc/xinetd.d/hell && \
    chmod 100 ./xinetd_start.sh

CMD [ "./xinetd_start.sh" ]

EXPOSE 9999
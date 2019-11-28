FROM python:3.7

ENV PYTHONUNBUFFERED 1

COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt

CMD [ "gunicorn", "-b", "0.0.0.0:9999", "-w", "4", "wsgi:app" ]
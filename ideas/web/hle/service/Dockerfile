FROM python:3.7

ENV PYTHONUNBUFFERED 1

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt
ENV FLASK_APP=wsgi.py
ENV FLASK_ENV=production

CMD [ "python", "-m", "flask", "run", "--host=0.0.0.0", "--port=9999" ]